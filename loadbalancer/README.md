# Loadbalancer

## Baixar o Elixir.
```bash
$ sudo add-apt-repository ppa:rabbitmq/rabbitmq-erlang
$ sudo apt update
$ sudo apt install git elixir erlang
```

## Como criar um "projeto" em elixir
```elixir
mix new nome_do_projeto
```

## Como rodar o LoadBalancer em elixir
* Após criar o projeto
* cd "NomeProjeto"
* touch lib/"nomearquivo".ex
* adicionar o chumak(versão do zeromq do Elixir) ao mix.exs
    * em "defp deps do" cole "{:chumak, "~> 1.5"}"
    * ```elixir
      def deps do
      [
        {:loadbalancer, "~> 0.1.0"}
      ]
      end
      ```
    No terminal, digite mix deps.get para baixar a biblioteca.
* Escreva o código.
* No terminal digite "iex -S mix" para compilar, isso abrirá um terminal especial "iex(1)>"
* digite "nomedoDefModule"."nomefunçãoprincipal" para rodar o código. (Ex: LoadBalancer.start)

# PONTOS IMPORTANTES
* No início, quando ocorre um erro, é por conta de o LoadBalancer estar procurando portas para se conectar, isso é normal e ele está funcionando normalmente.
* Os testes foram realizados no github codespace e também no ubuntu 22.04.0
* Os testes com Elixir foram realizados com o cliente.py e servidor.py

### Documentação.
* [ExDoc](https://github.com/elixir-lang/ex_doc)
* [HexDocs](https://hexdocs.pm)
* <https://hexdocs.pm/loadbalancer>

