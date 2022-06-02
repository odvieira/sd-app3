## Cliente
A forma mais simples de executar o cliente é usar o módulo *serve* para hospedar o cliente com o node. Instalável com o gerenciador de pacotes *yarn*.

		$ yarn global add serve
		$ serve -s build
	
Não é necessário escolher endereço, o *serve* sempre instancia em um endereço disponível.

## Servidor
O projeto Pipenv está completo aqui, basta executar:

		$ pipenv install
		$ pipenv run start

Ou então executar o interpretador python sobre o arquivo controller.py.

**Obseração:** Como *flask* é uma biblioteca single *thread*, é relativamente simples bloquear o fluxo de processamento com requisições completamente síncronas, por isso mantive minha decisão de estabelecer o fluxo padrão de resposta por notificação, deixando o retorno do método como *ack* apenas (*200 'OK'*). O aplicativo não apresentou qualquer lentidão nos testes realizados.

## Dependência
O projeto depende de uma middleware que gerencia o streaming dos dados. O servidor Redis precisa estar em execução quando o controller.py for interpretado. Existem versões binárias disponíveis em https://redis.io/download/. A versão utilizada no desenvolvimento desse app foi instalada automaticamente sem compilação do código fonte.