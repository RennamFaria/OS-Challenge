import os
import random

#qntProcess = 4
#div = [100, 200, 300, 400 ]
#numb= [random.randint(1, 100) for _ in range(400)]

class SumFork:
  def __init__(self, qntProcess, div, numb):
    self.qntProcess = qntProcess
    self.div = div
    self.numb = numb

  def SumAllParent(self):
    divided = self.DivideNumb()    #divide em sublistas
    pipes = []

    # Criar pipes
    for _ in range(self.qntProcess):
      r, w = os.pipe()
      pipes.append((r, w))

    processes = []

    for i in range(self.qntProcess):
      PID = os.fork()

      if PID == 0:  # Processo filho
        partial_sum = self.SumAll(divided[i])
        os.close(pipes[i][0])  # Fechar leitura do pipe
        os.write(pipes[i][1], str(partial_sum).encode())  # Escrever a soma parcial no pipe
        os.close(pipes[i][1])  # Fechar escrita do pipe
        os._exit(0)

      else:  # Processo pai
        processes.append(PID)

    # Processo pai aguarda e coleta resultados dos processos filhos
    total_sum = 0
    for i in range(self.qntProcess):
      os.close(pipes[i][1])  # Fechar escrita do pipe
      partial_sum = int(os.read(pipes[i][0],1024).decode())  # Ler a soma parcial do pipe
      total_sum += partial_sum
      os.close(pipes[i][0])  # Fechar leitura do pipe

    return total_sum

  def SumAll(self, numb):
    return sum(numb)

  def DivideNumb(self):
    divided = []
    for i in range(len(self.div)):
      if i == 0:
        start = 0
      else:
        start = self.div[i - 1]
      end = self.div[i]
      divided.append(self.Separate(start, end))
    return divided

  def Separate(self, start, end):
    return self.numb[start:end]


def main():
  qntProcess = 4  # Quantidade de processos
  div = [100, 200, 300, 400]  # Intervalo de cada fork para somar
  numb = [random.randint(1, 100) for _ in range(400)]  # Lista de números a serem somados

  print(numb)

  sum_fork = SumFork(qntProcess, div, numb)
  result = sum_fork.SumAllParent()
  print(f"\nThe Total Sum is equal to: {result}")

  print()
  print(sum(numb))


if __name__ == "__main__":
  main()
