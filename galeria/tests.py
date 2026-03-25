from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from galeria.models import Fotografia


class GaleriaViewsTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.fotografia = Fotografia.objects.create(
            nome='Nebulosa de Orion',
            legenda='Uma nebulosa famosa',
            categoria='NEBULOSA',
            descricao='Descrição da nebulosa de Orion',
            publicada=True,
            usuario=self.usuario,
        )

    def test_index_redireciona_usuario_nao_autenticado(self):
        response = self.client.get(reverse('index'))
        self.assertRedirects(response, '/login?next=/')

    def test_index_exibe_fotografias_publicadas(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nebulosa de Orion')

    def test_index_nao_exibe_fotografias_nao_publicadas(self):
        self.client.login(username='testuser', password='testpass123')
        Fotografia.objects.create(
            nome='Foto Oculta',
            legenda='Não publicada',
            categoria='ESTRELA',
            descricao='Esta foto não deve aparecer',
            publicada=False,
            usuario=self.usuario,
        )
        response = self.client.get(reverse('index'))
        self.assertNotContains(response, 'Foto Oculta')

    def test_imagem_redireciona_usuario_nao_autenticado(self):
        response = self.client.get(reverse('imagem', args=[self.fotografia.pk]))
        self.assertRedirects(
            response, f'/login?next=/imagem/{self.fotografia.pk}'
        )

    def test_imagem_exibe_detalhes_da_fotografia(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('imagem', args=[self.fotografia.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nebulosa de Orion')

    def test_imagem_retorna_404_para_foto_inexistente(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('imagem', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_buscar_redireciona_usuario_nao_autenticado(self):
        response = self.client.get(reverse('buscar'))
        self.assertRedirects(response, '/login?next=/buscar/')

    def test_buscar_retorna_resultados_por_nome(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('buscar'), {'buscar': 'Nebulosa'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nebulosa de Orion')

    def test_buscar_sem_resultado(self):
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('buscar'), {'buscar': 'inexistente'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Nebulosa de Orion')


class FotografiaModelTest(TestCase):
    def setUp(self):
        self.usuario = User.objects.create_user(
            username='testuser', password='testpass123'
        )

    def test_str_retorna_nome_da_fotografia(self):
        foto = Fotografia.objects.create(
            nome='Galaxia Andrômeda',
            legenda='Galáxia espiral',
            categoria='GALAXIA',
            descricao='A galáxia mais próxima da Via Láctea',
            usuario=self.usuario,
        )
        self.assertEqual(str(foto), 'Galaxia Andrômeda')

    def test_publicada_false_por_padrao(self):
        foto = Fotografia.objects.create(
            nome='Planeta Saturno',
            legenda='Planeta dos anéis',
            categoria='PLANETA',
            descricao='Saturno e seus anéis',
            usuario=self.usuario,
        )
        self.assertFalse(foto.publicada)
