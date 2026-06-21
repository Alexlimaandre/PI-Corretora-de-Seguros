# Roadmap de Migração: Desktop → Django
## Frank Costa Corretora de Seguros

> **Papel assumido:** Arquiteto de Software Sênior · Tech Lead Python/Django · Mentor de Carreira  
> **Perfil do desenvolvedor:** Intermediário em Python e SQL · Básico em Django · Foco em Dados e Backend  
> **Estratégia:** Migração gradual com aprendizado integrado — nenhuma etapa é pulada

---

## Visão Geral das Sprints

| Sprint | Tema | Dificuldade | Tempo |
|--------|------|-------------|-------|
| 1 | Fundação Django + Ambiente | Fácil | 4 dias |
| 2 | Models e Banco de Dados | Fácil/Intermediário | 5 dias |
| 3 | CRUD de Clientes (Views + Templates) | Intermediário | 6 dias |
| 4 | Login e Autenticação | Intermediário | 4 dias |
| 5 | CRUD Completo (Seguradoras, Planos, Bens) | Intermediário | 7 dias |
| 6 | Cotações e Apólices | Intermediário | 6 dias |
| 7 | Dashboard BI | Intermediário/Avançado | 7 dias |
| 8 | API REST e Qualidade | Intermediário/Avançado | 6 dias |
| 9 | Deploy no Render + Supabase | Intermediário | 4 dias |

**Estimativa total realista: 7 a 10 semanas** (com ~2 horas/dia útil de dedicação)

---

## Sprint 1 — Fundação Django + Ambiente

### Objetivo
Sair do zero absoluto com Django e ter o projeto criado, rodando localmente, conectado ao PostgreSQL existente. Você vai entender como o Django organiza um projeto e por que essa estrutura existe.

### Conceitos Django que você precisa estudar antes
- O que é MTV (Model · Template · View) e como difere do MVC
- Diferença entre **projeto** e **app** no Django
- O arquivo `settings.py` e para que serve cada bloco
- O que é o `manage.py` e seus comandos principais
- Como o Django faz roteamento via `urls.py`

### Funcionalidades da Sprint
- Ambiente virtual configurado com `venv`
- Projeto Django criado (`corretora_project`)
- App principal criado (`core`)
- PostgreSQL conectado via `settings.py`
- Página inicial "em branco" rodando no browser
- `.env` com variáveis de ambiente (senha do banco, secret key)

### Estrutura Técnica

```
corretora_project/
│
├── manage.py
├── .env                          ← credenciais fora do código
├── requirements.txt
│
├── corretora_project/
│   ├── settings.py               ← configuração do projeto
│   ├── urls.py                   ← rotas raiz
│   └── wsgi.py
│
└── core/                         ← app principal
    ├── views.py
    ├── urls.py
    └── templates/
        └── core/
            └── index.html
```

### Banco de Dados
Nesta sprint você **não altera** o banco. Apenas configura o Django para apontar para o PostgreSQL existente (`Frank_Costa`) usando `psycopg2-binary` e `python-decouple` para variáveis de ambiente.

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT', default='5432'),
    }
}
```

### Critérios de Conclusão
- [ ] `python manage.py runserver` sobe sem erros
- [ ] `python manage.py dbshell` conecta no PostgreSQL
- [ ] Página inicial abre no browser em `localhost:8000`
- [ ] Nenhuma senha está hardcoded no código

### Dificuldade: Fácil
### Tempo estimado: 4 dias

---

## Sprint 2 — Models e Banco de Dados

### Objetivo
Traduzir as tabelas SQL existentes para Models Django. Entender o ORM do Django e como ele se relaciona com o banco real. Esta sprint é o coração da migração — acertar os models agora poupa retrabalho em tudo que vem depois.

### Conceitos Django que você precisa estudar antes
- O que é um **Model** e como ele mapeia para uma tabela SQL
- Tipos de campo: `CharField`, `IntegerField`, `DateField`, `DecimalField`, `ForeignKey`
- `ForeignKey` e `on_delete` — o que acontece quando um registro pai é deletado
- O que são **migrações** (`makemigrations` e `migrate`) e por que existem
- `Meta class` nos models: `db_table`, `ordering`, `verbose_name`
- A opção `managed = False` — usar tabelas existentes sem que o Django as recrie

### Funcionalidades da Sprint
- Todos os models mapeados para as tabelas existentes
- Migrations criadas **sem destruir os dados** (`managed = False` inicialmente)
- Shell Django testando queries no banco real
- Admin Django básico configurado para visualizar os dados

### Estrutura Técnica

```
core/
├── models.py         ← todos os models aqui
├── admin.py          ← registro no painel admin
└── migrations/
    └── 0001_initial.py
```

### Banco de Dados — Tradução das Tabelas para Models

```python
# core/models.py

class Pessoa(models.Model):
    id_pessoa       = models.AutoField(primary_key=True)
    cpf_cnpj        = models.CharField(max_length=14, unique=True)
    nome_completo   = models.CharField(max_length=150)
    email           = models.EmailField(blank=True, null=True)
    sexo            = models.CharField(max_length=1, blank=True, null=True)
    telefone        = models.CharField(max_length=11, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    status          = models.CharField(max_length=20, default='Ativo')

    class Meta:
        db_table = 'pessoa'
        verbose_name = 'Cliente'

class Seguradora(models.Model):
    id_seguradora    = models.AutoField(primary_key=True)
    nome_fantasia    = models.CharField(max_length=100)
    cnpj             = models.CharField(max_length=14, unique=True)
    telefone_suporte = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        db_table = 'seguradora'

class Plano(models.Model):
    id_plano       = models.AutoField(primary_key=True)
    id_seguradora  = models.ForeignKey(Seguradora, on_delete=models.PROTECT,
                                       db_column='id_seguradora')
    tipo_cobertura = models.CharField(max_length=50)
    nome_plano     = models.CharField(max_length=100)

    class Meta:
        db_table = 'plano'

class Bens(models.Model):
    id_bem         = models.AutoField(primary_key=True)
    id_pessoa      = models.ForeignKey(Pessoa, on_delete=models.CASCADE,
                                       db_column='id_pessoa')
    tipo_bem       = models.CharField(max_length=50)
    descricao_bem  = models.CharField(max_length=255)
    valor_estimado = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = 'bens'

class Cotacoes(models.Model):
    id_cotacao     = models.AutoField(primary_key=True)
    id_pessoa      = models.ForeignKey(Pessoa, on_delete=models.PROTECT,
                                       db_column='id_pessoa')
    id_seguradora  = models.ForeignKey(Seguradora, on_delete=models.PROTECT,
                                       db_column='id_seguradora')
    id_plano       = models.ForeignKey(Plano, on_delete=models.PROTECT,
                                       db_column='id_plano')
    valor_cotacao  = models.DecimalField(max_digits=12, decimal_places=2)
    data_cotacao   = models.DateField()
    status_cotacao = models.CharField(max_length=30, default='Pendente')

    class Meta:
        db_table = 'cotacoes'

class Apolice(models.Model):
    id_apolice = models.AutoField(primary_key=True)
    id_cotacao = models.OneToOneField(Cotacoes, on_delete=models.PROTECT,
                                      db_column='id_cotacao')
    inicio     = models.DateField()
    fim        = models.DateField()

    class Meta:
        db_table = 'apolice'

class Usuario(models.Model):
    id_usuario    = models.AutoField(primary_key=True)
    nome_usuario  = models.CharField(max_length=80, unique=True)
    senha         = models.CharField(max_length=255)

    class Meta:
        db_table = 'usuario'
```

### Critérios de Conclusão
- [ ] `python manage.py makemigrations` roda sem erros
- [ ] `python manage.py migrate` não altera os dados existentes
- [ ] No Django shell: `Pessoa.objects.count()` retorna o número correto de clientes
- [ ] Painel `/admin` exibe os registros de todas as tabelas

### Dificuldade: Fácil/Intermediário
### Tempo estimado: 5 dias

---

## Sprint 3 — CRUD de Clientes (Views + Templates)

### Objetivo
Implementar o CRUD completo de Clientes na web. Esta é a sprint mais densa em conceitos novos, pois você vai aprender o ciclo completo de uma requisição web no Django: URL → View → Template → Banco → Template.

### Conceitos Django que você precisa estudar antes
- **Function-based views (FBV):** como uma função recebe um `request` e retorna um `response`
- `render()`, `redirect()`, `get_object_or_404()`
- **Django Forms:** o que são, como criar, como validar (`form.is_valid()`)
- **Context:** como passar dados da view para o template
- **Template Language:** `{{ variavel }}`, `{% for %}`, `{% if %}`, `{% url %}`, `{% csrf_token %}`
- `request.method == 'POST'` vs `GET` — o ciclo de um formulário web
- **Mensagens flash** com `django.contrib.messages`

### Funcionalidades da Sprint
- Listagem de clientes com busca por nome e CPF
- Cadastro de novo cliente
- Edição de cliente existente
- Exclusão com confirmação
- Mensagens de sucesso e erro inline
- Layout base com menu lateral (equivalente ao sistema desktop)

### Estrutura Técnica

```
core/
├── views/
│   ├── __init__.py
│   └── clientes.py        ← views separadas por domínio
├── forms/
│   ├── __init__.py
│   └── cliente_form.py
├── urls.py
└── templates/
    ├── base.html           ← layout base com navbar e sidebar
    └── clientes/
        ├── lista.html
        ├── form.html       ← usado para criar e editar
        └── confirmar_exclusao.html
```

### Exemplo de View (padrão que você vai repetir para cada entidade)

```python
# core/views/clientes.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from core.models import Pessoa
from core.forms.cliente_form import ClienteForm

def lista_clientes(request):
    busca = request.GET.get('q', '')
    clientes = Pessoa.objects.all()
    if busca:
        clientes = clientes.filter(nome_completo__icontains=busca)
    return render(request, 'clientes/lista.html', {'clientes': clientes, 'busca': busca})

def criar_cliente(request):
    form = ClienteForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente cadastrado com sucesso!')
        return redirect('lista_clientes')
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Novo Cliente'})

def editar_cliente(request, pk):
    cliente = get_object_or_404(Pessoa, pk=pk)
    form = ClienteForm(request.POST or None, instance=cliente)
    if form.is_valid():
        form.save()
        messages.success(request, 'Cliente atualizado!')
        return redirect('lista_clientes')
    return render(request, 'clientes/form.html', {'form': form, 'titulo': 'Editar Cliente'})

def deletar_cliente(request, pk):
    cliente = get_object_or_404(Pessoa, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente removido.')
        return redirect('lista_clientes')
    return render(request, 'clientes/confirmar_exclusao.html', {'cliente': cliente})
```

### Banco de Dados
Apenas leitura e escrita via ORM. Nenhuma query SQL manual necessária nesta sprint.

### Critérios de Conclusão
- [ ] `/clientes/` lista todos os clientes
- [ ] Campo de busca filtra por nome e CPF
- [ ] `/clientes/novo/` cria um cliente e redireciona para a lista
- [ ] `/clientes/editar/1/` carrega os dados e permite alterar
- [ ] Exclusão exige confirmação antes de deletar
- [ ] Mensagens de feedback aparecem corretamente

### Dificuldade: Intermediário
### Tempo estimado: 6 dias

---

## Sprint 4 — Login e Autenticação

### Objetivo
Proteger o sistema com autenticação. Reutilizar a tabela `usuario` existente ou migrar para o sistema de autenticação nativo do Django. Você vai entender sessões, decorators e controle de acesso.

### Conceitos Django que você precisa estudar antes
- O sistema de autenticação nativo do Django (`django.contrib.auth`)
- `User` model padrão vs model customizado
- `login()`, `logout()`, `authenticate()` do Django
- O decorator `@login_required` e como ele redireciona
- **Sessões:** como o Django mantém o usuário logado entre requisições
- `LoginRequiredMixin` para Class-Based Views (introdução)

### Funcionalidades da Sprint
- Tela de login com identidade visual Frank Costa
- Logout funcional
- Todas as rotas do sistema protegidas por autenticação
- Redirecionamento automático para login quando não autenticado
- Opção A: usar tabela `usuario` existente com autenticação manual
- Opção B (recomendada): migrar para `django.contrib.auth.User`

### Estrutura Técnica

```
core/
├── views/
│   └── auth.py             ← login e logout
└── templates/
    └── auth/
        └── login.html
```

### Por que a Opção B é recomendada?
O Django tem um sistema de auth robusto com hash de senha, grupos de permissão e integração com o admin. Usar a tabela `usuario` manual com senha em texto puro é uma falha de segurança. Nesta sprint você vai criar um superusuário Django e deprecar a tabela antiga.

```python
# views/auth.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def view_login(request):
    if request.method == 'POST':
        user = authenticate(
            request,
            username=request.POST['usuario'],
            password=request.POST['senha']
        )
        if user:
            login(request, user)
            return redirect('lista_clientes')
        return render(request, 'auth/login.html', {'erro': 'Usuário ou senha inválidos'})
    return render(request, 'auth/login.html')

def view_logout(request):
    logout(request)
    return redirect('login')
```

### Critérios de Conclusão
- [ ] Acessar `/clientes/` sem estar logado redireciona para `/login/`
- [ ] Login com credenciais válidas redireciona para o sistema
- [ ] Logout volta para a tela de login
- [ ] Senha armazenada com hash (não em texto puro)

### Dificuldade: Intermediário
### Tempo estimado: 4 dias

---

## Sprint 5 — CRUD Completo (Seguradoras, Planos, Bens)

### Objetivo
Repetir o padrão da Sprint 3 para as demais entidades. O foco agora é **velocidade e consolidação** — você já conhece o ciclo, então vai executar mais rápido e perceber os padrões que se repetem. Também vai aprender a lidar com relacionamentos nos formulários.

### Conceitos Django que você precisa estudar antes
- `ModelForm` — geração automática de formulários a partir dos models
- `ForeignKey` em formulários: `ModelChoiceField` e como renderizar um `<select>`
- **Reutilização de templates:** um `form.html` genérico para todos os CRUDs
- `Q objects` para buscas com múltiplos filtros (`Q(campo1=x) | Q(campo2=y)`)
- `order_by()` e `filter()` com lookups do ORM (`__icontains`, `__gte`, `__lte`)

### Funcionalidades da Sprint
- CRUD completo de Seguradoras
- CRUD completo de Planos (com select de seguradora)
- CRUD completo de Bens (com select de cliente/proprietário)
- Template genérico reutilizável para formulários
- Busca em todas as listagens

### Estrutura Técnica

```
core/
├── views/
│   ├── seguradoras.py
│   ├── planos.py
│   └── bens.py
├── forms/
│   ├── seguradora_form.py
│   ├── plano_form.py
│   └── bem_form.py
└── templates/
    ├── seguradoras/
    ├── planos/
    └── bens/
```

### Padrão de URL que você vai adotar (RESTful)

```python
# urls.py — padrão para cada entidade
path('seguradoras/',              views.lista_seguradoras,  name='lista_seguradoras'),
path('seguradoras/nova/',         views.criar_seguradora,   name='criar_seguradora'),
path('seguradoras/<int:pk>/',     views.detalhe_seguradora, name='detalhe_seguradora'),
path('seguradoras/<int:pk>/editar/',  views.editar_seguradora, name='editar_seguradora'),
path('seguradoras/<int:pk>/deletar/', views.deletar_seguradora, name='deletar_seguradora'),
```

### Critérios de Conclusão
- [ ] CRUD funcional para Seguradoras, Planos e Bens
- [ ] Formulário de Plano exibe select com seguradoras cadastradas
- [ ] Formulário de Bem exibe select com clientes cadastrados
- [ ] Busca funciona em todas as listagens
- [ ] Nenhuma lógica de banco está fora dos models/views (sem SQL manual)

### Dificuldade: Intermediário
### Tempo estimado: 7 dias

---

## Sprint 6 — Cotações e Apólices

### Objetivo
Implementar as entidades mais complexas do sistema. Cotações e apólices têm regras de negócio (aprovação gera apólice automaticamente) que hoje são feitas por trigger no banco. Você vai aprender a trazer essa lógica para o Django ou mantê-la no banco com sinais (`signals`).

### Conceitos Django que você precisa estudar antes
- **Signals:** `post_save`, `pre_delete` — como o Django reage a eventos do banco
- **Transactions:** `transaction.atomic()` — garantir que operações relacionadas são atômicas
- `select_related()` e `prefetch_related()` — evitar o problema N+1 de queries
- Formulários com múltiplos steps ou dependências entre campos
- **Class-Based Views (introdução):** `ListView`, `CreateView`, `UpdateView`, `DeleteView`

### Funcionalidades da Sprint
- CRUD completo de Cotações
- Mudança de status da cotação (Pendente → Aprovada → Apólice gerada)
- Geração automática de apólice quando cotação é aprovada (via signal ou view)
- CRUD de Apólices com visualização detalhada
- Listagem de apólices vencidas e vencendo em breve

### Lógica de Geração de Apólice via Signal

```python
# core/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Cotacoes, Apolice
from datetime import date, timedelta

@receiver(post_save, sender=Cotacoes)
def gerar_apolice_automatica(sender, instance, **kwargs):
    if instance.status_cotacao == 'Aprovada':
        # Só cria se ainda não existir apólice para esta cotação
        if not hasattr(instance, 'apolice'):
            Apolice.objects.create(
                id_cotacao=instance,
                inicio=date.today(),
                fim=date.today() + timedelta(days=365)
            )
```

### Critérios de Conclusão
- [ ] CRUD de Cotações funcional com filtro por status
- [ ] Mudar status de uma cotação para "Aprovada" cria a apólice automaticamente
- [ ] CRUD de Apólices com datas de vigência
- [ ] Listagem de apólices vencidas (fim < hoje)
- [ ] Listagem de apólices vencendo nos próximos 30 dias

### Dificuldade: Intermediário
### Tempo estimado: 6 dias

---

## Sprint 7 — Dashboard BI

### Objetivo
Recriar o Dashboard BI do sistema desktop como uma página web dinâmica. Esta sprint é o maior salto de complexidade visual, mas a lógica de dados você já conhece — está toda no `crud.py` original. Aqui você vai aprender a passar dados agregados para gráficos no frontend.

### Conceitos Django que você precisa estudar antes
- `aggregate()` e `annotate()` do ORM — equivalente ao `GROUP BY` e `COUNT` do SQL
- `values()` com `annotate()` — agrupamentos com o ORM
- **Django como API:** retornar JSON em uma view (`JsonResponse`)
- Como integrar uma biblioteca de gráficos JavaScript (Chart.js) com dados do Django
- Context processors — passar dados globais para todos os templates

### Funcionalidades da Sprint
- Card de Clientes por Status
- Card de Cotações no período
- Card de Novas Apólices
- Card de Apólices Vencidas e Vencendo
- Card de Taxa de Conversão
- Ranking de Seguradoras com barra de progresso
- Filtros de período e status via AJAX (sem recarregar a página)

### Estrutura Técnica

```
core/
├── views/
│   └── dashboard.py        ← views do BI
├── services/
│   └── bi_service.py       ← lógica de cálculo separada da view
└── templates/
    └── dashboard/
        └── index.html
```

### Separação de Responsabilidades (padrão profissional)

```python
# core/services/bi_service.py
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import timedelta
from core.models import Pessoa, Cotacoes, Apolice, Seguradora

class BIService:

    @staticmethod
    def clientes_por_status(status='Ativo'):
        return Pessoa.objects.filter(status__iexact=status).count()

    @staticmethod
    def novas_cotacoes(dias=30):
        corte = timezone.now().date() - timedelta(days=dias)
        return Cotacoes.objects.filter(data_cotacao__gte=corte).count()

    @staticmethod
    def apolices_vencendo(dias=30):
        hoje = timezone.now().date()
        return Apolice.objects.filter(
            fim__gte=hoje,
            fim__lte=hoje + timedelta(days=dias)
        ).count()

    @staticmethod
    def ranking_seguradoras():
        return (
            Seguradora.objects
            .annotate(qtd_contratos=Count('cotacoes__apolice'))
            .values('nome_fantasia', 'qtd_contratos')
            .order_by('-qtd_contratos')[:8]
        )
```

### Critérios de Conclusão
- [ ] Dashboard carrega com os 6 cards de indicadores
- [ ] Ranking de seguradoras exibe barra de progresso proporcional
- [ ] Filtro de período atualiza os cards sem recarregar a página
- [ ] Leitura gerencial exibe texto dinâmico com os números atuais
- [ ] `bi_service.py` separado da view (testável de forma isolada)

### Dificuldade: Intermediário/Avançado
### Tempo estimado: 7 dias

---

## Sprint 8 — API REST e Qualidade

### Objetivo
Expor os dados do sistema como uma API REST usando Django REST Framework. Esta sprint prepara o sistema para integrações futuras e é um diferencial enorme de portfólio. Também é o momento de adicionar testes automatizados básicos.

### Conceitos Django que você precisa estudar antes
- O que é uma API REST e por que ela importa
- **Django REST Framework (DRF):** instalação e configuração
- `Serializers` — equivalente aos Forms, mas para JSON
- `ViewSets` e `Routers` — geração automática de endpoints CRUD
- `APIView` e `@api_view` para endpoints customizados
- Testes com `TestCase` do Django e `APITestCase` do DRF
- Autenticação de API: `TokenAuthentication` vs `SessionAuthentication`

### Funcionalidades da Sprint
- Endpoints REST para Clientes, Seguradoras, Planos, Bens, Cotações e Apólices
- Endpoint de indicadores BI em JSON (`/api/bi/indicadores/`)
- Documentação automática com Swagger/drf-spectacular
- Testes básicos de CRUD para o model `Pessoa`
- Paginação de resultados

### Estrutura Técnica

```
api/                           ← novo app exclusivo para a API
├── serializers.py
├── views.py
├── urls.py
└── tests.py
```

### Exemplo de Serializer e ViewSet

```python
# api/serializers.py
from rest_framework import serializers
from core.models import Pessoa

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoa
        fields = '__all__'

# api/views.py
from rest_framework.viewsets import ModelViewSet
from core.models import Pessoa
from .serializers import PessoaSerializer

class PessoaViewSet(ModelViewSet):
    queryset = Pessoa.objects.all().order_by('nome_completo')
    serializer_class = PessoaSerializer
    filterset_fields = ['status', 'sexo']
    search_fields = ['nome_completo', 'cpf_cnpj']
```

### Critérios de Conclusão
- [ ] `GET /api/clientes/` retorna lista paginada em JSON
- [ ] `POST /api/clientes/` cria um cliente via JSON
- [ ] `GET /api/bi/indicadores/` retorna os 6 indicadores do dashboard
- [ ] Swagger acessível em `/api/docs/`
- [ ] Pelo menos 5 testes automatizados passando

### Dificuldade: Intermediário/Avançado
### Tempo estimado: 6 dias

---

## Sprint 9 — Deploy no Render + Supabase

### Objetivo
Colocar o sistema em produção. Você vai aprender a diferença entre ambiente local e produção, como configurar variáveis de ambiente, banco de dados em nuvem e servir arquivos estáticos corretamente.

### Conceitos Django que você precisa estudar antes
- `DEBUG = False` e suas implicações de segurança
- `ALLOWED_HOSTS` — por que é necessário em produção
- **Arquivos estáticos em produção:** `whitenoise` para servir CSS/JS/imagens
- Variáveis de ambiente com `python-decouple` ou `os.environ`
- `gunicorn` — servidor WSGI para produção (o `runserver` não serve para produção)
- Como criar um banco PostgreSQL no Supabase e conectar ao Django
- `Procfile` — como o Render sabe como iniciar a aplicação

### Funcionalidades da Sprint
- Banco PostgreSQL migrado para Supabase (ou mantido local com acesso externo)
- Aplicação Django deployada no Render
- Variáveis de ambiente configuradas no painel do Render
- Arquivos estáticos servidos corretamente
- HTTPS automático pelo Render
- `collectstatic` configurado corretamente

### Arquivos de Configuração para Produção

```python
# settings.py (versão produção)
import os
from decouple import config

DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

```
# Procfile (na raiz do projeto)
web: gunicorn corretora_project.wsgi --log-file -
```

### Critérios de Conclusão
- [ ] Sistema acessível via URL pública do Render
- [ ] Login funcionando com dados reais do banco
- [ ] Nenhuma credencial exposta no código (tudo em variáveis de ambiente)
- [ ] Arquivos estáticos (CSS, JS) carregando corretamente em produção
- [ ] HTTPS funcionando

### Dificuldade: Intermediário
### Tempo estimado: 4 dias

---

## Arquitetura Final do Sistema Django

```
corretora_project/                  ← raiz do projeto
│
├── manage.py
├── requirements.txt
├── Procfile                        ← instrução de deploy (Render)
├── .env                            ← variáveis locais (não vai para o Git)
│
├── corretora_project/              ← configurações globais
│   ├── settings/
│   │   ├── base.py                 ← configurações comuns
│   │   ├── development.py          ← apenas para local
│   │   └── production.py           ← apenas para Render
│   ├── urls.py
│   └── wsgi.py
│
├── core/                           ← app principal (UI e regras de negócio)
│   ├── models.py
│   ├── admin.py
│   ├── signals.py
│   ├── forms/
│   │   ├── cliente_form.py
│   │   ├── seguradora_form.py
│   │   ├── plano_form.py
│   │   ├── bem_form.py
│   │   ├── cotacao_form.py
│   │   └── apolice_form.py
│   ├── views/
│   │   ├── auth.py
│   │   ├── clientes.py
│   │   ├── seguradoras.py
│   │   ├── planos.py
│   │   ├── bens.py
│   │   ├── cotacoes.py
│   │   ├── apolices.py
│   │   └── dashboard.py
│   ├── services/
│   │   └── bi_service.py           ← lógica de BI isolada e testável
│   ├── templates/
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── clientes/
│   │   ├── seguradoras/
│   │   ├── planos/
│   │   ├── bens/
│   │   ├── cotacoes/
│   │   ├── apolices/
│   │   └── dashboard/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   └── tests/
│       ├── test_models.py
│       ├── test_views.py
│       └── test_services.py
│
└── api/                            ← app da API REST (DRF)
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── tests.py
```

### Fluxo de uma Requisição na Arquitetura Final

```
Browser → urls.py → View → Service (BI) / Form (validação) → Model (ORM) → PostgreSQL
                       ↓
                  Template → HTML renderizado → Browser
```

---

## Estimativa Total Realista

| Fase | Sprints | Dias úteis |
|------|---------|------------|
| Fundação e Banco | 1 e 2 | 9 dias |
| CRUDs e Auth | 3, 4 e 5 | 17 dias |
| Entidades complexas e BI | 6 e 7 | 13 dias |
| API e Deploy | 8 e 9 | 10 dias |
| **Total** | **9 sprints** | **~49 dias úteis** |

Com ~2 horas por dia útil: **entre 7 e 10 semanas** de trabalho consistente.

> **Dica de carreira:** não espere terminar tudo para colocar no portfólio. A partir da Sprint 4 (sistema com login funcionando), já é um projeto apresentável. A Sprint 8 (com API e testes) é o nível que diferencia candidatos a vagas de backend júnior.

---

## Tecnologias e Dependências do Projeto Final

```
# requirements.txt
Django==4.2
psycopg2-binary==2.9
python-decouple==3.8
gunicorn==21.2
whitenoise==6.6
djangorestframework==3.15
drf-spectacular==0.27       # Swagger automático
django-filter==24.1         # Filtros nas listagens e na API
```

---

*Roadmap elaborado para o sistema Frank Costa Corretora de Seguros*  
*Versão 1.0 · Junho 2026*