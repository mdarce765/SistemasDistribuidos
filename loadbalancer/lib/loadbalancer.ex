defmodule LoadBalancer do
  @moduledoc """
  LoadBalancer em Elixir usando Chumak para balanceamento de mensagens entre sockets ZeroMQ.
  """
def checarUso do
  Enum.reduce(Enum.take_every(5559..5600, 2), [], fn x, servidores ->
    {:ok, socket} = :chumak.socket(:push)
    case :chumak.bind(socket, :tcp, ~c"0.0.0.0", x) do
      {:ok, _pid} ->
        servidores
      _err ->
        IO.puts("Porta #{x} ja ocupada, tentando a próxima.")
        servidores ++ [[x, x + 1]]
    end
  end)
end

  def start do
    ultimoUsado = -1
    servidores = checarUso()
    IO.inspect("lista servidores #{inspect(servidores)}")
    IO.inspect("Quantidade de servidores #{length(servidores)}")
    IO.puts("Iniciando LoadBalancer...")

    # Criação dos sockets
    {:ok, pull} = :chumak.socket(:pull)
    {:ok, push} = :chumak.socket(:push)
    {:ok, rep} = :chumak.socket(:rep)
    {:ok, req} = :chumak.socket(:req)
    {:ok, pub} = :chumak.socket(:pub)
    {:ok, sub} = :chumak.socket(:sub)

    # Bind dos sockets
    case :chumak.bind(pull, :tcp, ~c"0.0.0.0", 5555) do
      {:ok, _pid} ->
        IO.puts("PULL sucesso")
      _err ->
        checarUso()
    end
    case :chumak.bind(rep, :tcp, ~c"0.0.0.0", 5556) do
      {:ok, _pid} ->
        IO.puts("REP sucesso")
      _err ->
        checarUso()
    end
    case :chumak.bind(pub, :tcp, ~c"0.0.0.0", 5557) do
      {:ok, _pid} ->
        IO.puts("PUB sucesso")
      _err ->
        checarUso()
    end
    :chumak.subscribe(sub, <<>>)
    case :chumak.bind(sub, :tcp, ~c"localhost", 5558) do
      {:ok, _pid} ->
        IO.puts("SUB sucesso")
      _err ->
        checarUso()
    end
    # bind dos sockets

    spawn(fn -> loopPP(pull, push, servidores, ultimoUsado) end)
    spawn(fn -> loopRR(rep, req, servidores, ultimoUsado) end)
    spawn(fn -> loopPS(sub, pub) end)

    Process.sleep(:infinity)
  end

  defp loopPP(pull, push, servidores, ultimoUsado) do
    case :chumak.recv(pull) do
      {:ok, msg} ->
        servidoresDisp = servidores
        nultimo = rem((ultimoUsado + 1), length(servidoresDisp))
        porta = servidoresDisp |> Enum.at(ultimoUsado) |> Enum.at(0)
        :chumak.connect(push, :tcp, ~c"localhost", porta)
        :chumak.send(push, msg)
        IO.puts("push mandado #{msg}")
        loopPP(pull, push, servidores, nultimo)
    end
  end

  defp loopRR(rep, req, servidores, ultimoUsado) do
    case :chumak.recv(rep) do
      {:ok, msg} ->
        IO.puts("Req recebido #{inspect(msg)}")
        servidoresDisp = servidores
        nultimo = rem((ultimoUsado + 1), length(servidoresDisp))
        porta = servidoresDisp |> Enum.at(ultimoUsado) |> Enum.at(1)
        :chumak.connect(req, :tcp, ~c"localhost", porta)
        :chumak.send(req, msg)
        IO.puts("Req mandado #{msg}")
        case :chumak.recv(req) do
          {:ok, msgrep} ->
            IO.puts("Rep recebido #{inspect(msgrep)}")
            :chumak.send(rep, msgrep)
            IO.puts("Rep mandado #{msgrep}")
        end
      loopRR(rep, req, servidores, nultimo)
    end
  end

  defp loopPS(sub, pub) do
    case :chumak.recv(sub) do
      {:ok, msg} ->
        IO.puts("pub recebido #{inspect(msg)}")
        :chumak.send(pub, msg)
        IO.puts("pub mandado #{msg}")
    end
    loopPS(sub, pub)
  end
end