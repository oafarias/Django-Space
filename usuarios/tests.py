from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from usuarios.forms import LoginForms, CadastroForms


class LoginViewTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_login_exibe_formulario(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], LoginForms)

    def test_login_com_credenciais_validas(self):
        response = self.client.post(reverse('login'), {
            'nome_login': 'testuser',
            'senha': 'testpass123',
        })
        self.assertRedirects(response, reverse('index'))

    def test_login_com_credenciais_invalidas(self):
        response = self.client.post(reverse('login'), {
            'nome_login': 'testuser',
            'senha': 'senhaerrada',
        })
        self.assertRedirects(response, reverse('login'))

    def test_login_com_formulario_invalido(self):
        response = self.client.post(reverse('login'), {
            'nome_login': '',
            'senha': '',
        })
        self.assertEqual(response.status_code, 200)


class CadastroViewTest(TestCase):
    def test_cadastro_exibe_formulario(self):
        response = self.client.get(reverse('cadastro'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], CadastroForms)

    def test_cadastro_cria_usuario(self):
        response = self.client.post(reverse('cadastro'), {
            'nome_cadastro': 'novousuario',
            'email': 'novo@exemplo.com',
            'senha_1': 'SenhaForte123!',
            'senha_2': 'SenhaForte123!',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='novousuario').exists())

    def test_cadastro_senhas_diferentes(self):
        response = self.client.post(reverse('cadastro'), {
            'nome_cadastro': 'novousuario',
            'email': 'novo@exemplo.com',
            'senha_1': 'SenhaForte123!',
            'senha_2': 'SenhaDiferente!',
        })
        self.assertRedirects(response, reverse('cadastro'))
        self.assertFalse(User.objects.filter(username='novousuario').exists())

    def test_cadastro_usuario_duplicado(self):
        User.objects.create_user(username='existente', password='pass123')
        response = self.client.post(reverse('cadastro'), {
            'nome_cadastro': 'existente',
            'email': 'existente@exemplo.com',
            'senha_1': 'SenhaForte123!',
            'senha_2': 'SenhaForte123!',
        })
        self.assertRedirects(response, reverse('cadastro'))
        self.assertEqual(User.objects.filter(username='existente').count(), 1)


class LogoutViewTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_logout_encerra_sessao_e_redireciona(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/login?next=/')


class LoginFormsTest(TestCase):
    def test_formulario_valido(self):
        form = LoginForms(data={'nome_login': 'usuario', 'senha': 'senha123'})
        self.assertTrue(form.is_valid())

    def test_formulario_nome_vazio(self):
        form = LoginForms(data={'nome_login': '', 'senha': 'senha123'})
        self.assertFalse(form.is_valid())

    def test_formulario_senha_vazia(self):
        form = LoginForms(data={'nome_login': 'usuario', 'senha': ''})
        self.assertFalse(form.is_valid())


class CadastroFormsTest(TestCase):
    def test_formulario_valido(self):
        form = CadastroForms(data={
            'nome_cadastro': 'usuario',
            'email': 'usuario@exemplo.com',
            'senha_1': 'senha123',
            'senha_2': 'senha123',
        })
        self.assertTrue(form.is_valid())

    def test_formulario_email_invalido(self):
        form = CadastroForms(data={
            'nome_cadastro': 'usuario',
            'email': 'email-invalido',
            'senha_1': 'senha123',
            'senha_2': 'senha123',
        })
        self.assertFalse(form.is_valid())

    def test_formulario_campos_obrigatorios_vazios(self):
        form = CadastroForms(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('nome_cadastro', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('senha_1', form.errors)
        self.assertIn('senha_2', form.errors)
