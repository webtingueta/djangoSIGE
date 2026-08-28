.PHONY: help install install-dev run migrate makemigrations shell dbshell backup test testx

MANAGE = python manage.py

help:
	@echo "Comandos disponíveis:"
	@echo "  make install        Instala dependências de produção"
	@echo "  make install-dev    Instala dependências de desenvolvimento"
	@echo "  make run            Inicia o servidor de desenvolvimento"
	@echo "  make migrate        Executa as migrações (suporta ARGS=\"app_name\")"
	@echo "  make makemigrations Cria novas migrações (suporta ARGS=\"app_name\")"
	@echo "  make shell          Abre o shell interativo do Django"
	@echo "  make dbshell        Abre o shell de linha de comando do banco de dados"
	@echo "  make backup         Gera um backup dumpdata em db_backup.json"
	@echo "  make test           Executa testes com cobertura (suporta ARGS=\"-k nome\")"
	@echo "  make testx          Executa testes e para no primeiro erro"

# Instalação de Dependências
install:
	@pip install -r requirements.txt

install-dev: install
	@pip install -r requirements/dev.txt

# Servidor e Banco de Dados
run:
	@$(MANAGE) runserver

migrate:
	@$(MANAGE) migrate $(ARGS)

makemigrations:
	@$(MANAGE) makemigrations $(ARGS)

shell:
	@$(MANAGE) shell

dbshell:
	@$(MANAGE) dbshell

backup:
	@$(MANAGE) dumpdata > db_backup.json

# Testes
test:
	@pytest --cov $(ARGS)

testx:
	@pytest --cov -x $(ARGS)
