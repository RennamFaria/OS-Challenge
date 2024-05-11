#allProcess = [
#    Process(arrivalTime=0, duration=24),
#    Process(arrivalTime=1, duration=3),
#    Process(arrivalTime=2, duration=3),
#]

class Process:
  def __init__(self, arrivalTime, duration):
    self.arrivalTime = arrivalTime
    self.duration = duration
    self.remainingTime = duration
    self.waitingTime = 0
    self.responseTime = 0
    self.processTime = 0
    self.turnAround = 0


class ProcessSchedule:

  def __init__(self, allProcess):
    self.processes = allProcess
    self.counter = 0

  def FCFS(self):
    self.processes.sort(
      key=lambda x: x.arrivalTime)  #organiza por arrival time

    #calcula os tempos previamente dependendo do tempo de chegada
    for process in self.processes:
      process.waitingTime = self.counter - process.arrivalTime
      process.responseTime = self.counter - process.arrivalTime
      process.turnAround = self.counter + process.duration - process.arrivalTime
      process.processTime = process.turnAround - process.waitingTime
      self.DoProcess(process)

      self.counter += process.duration

  def RR(self, quantum):
    # Organiza os processos por tempo de chegada
    self.processes.sort(key=lambda x: x.arrivalTime)

    # Inicializa o tempo atual e uma lista para acompanhar processos prontos para execução
    self.counter = 0
    queue = []

    # Inicializa o índice do processo atual a ser examinado para adição à fila
    index = 0

    # Enquanto houver processos para processar
    while (queue) or (index < len(self.processes)):
      # Verifica se novos processos precisam ser adicionados à fila
      while (index < len(self.processes)):
        queue.append(self.processes[index])
        index += 1

      if queue:
        # Pega o próximo processo da fila
        process = queue.pop(0)
        self.DoProcess(process)

        # Calcula o tempo de execução para este ciclo
        time_slice = min(quantum, process.remainingTime)

        # Executa o processo por time_slice ou até ele terminar
        process.remainingTime -= time_slice
        self.counter += time_slice

        if process.responseTime == 0 and process.arrivalTime == 0:
          # Se é o primeiro processo, o responseTime é 0
          process.responseTime = process.arrivalTime

        elif process.responseTime == 0:
          process.responseTime = self.counter - process.arrivalTime - time_slice

        if process.remainingTime > 0:
          # Se ainda resta tempo, coloca de volta na fila
          queue.append(process)
        else:
          # Processo terminou, atualiza o tempo de espera e turnaround
          process.turnAround = self.counter - process.arrivalTime
          process.waitingTime = process.turnAround - process.duration
      else:
        # Se não há processos prontos, avança o tempo para a chegada do próximo processo
        self.counter = self.processes[index].arrivalTime
    for process in self.processes:
      process.processTime = process.turnAround - process.waitingTime

  def SJF(self):
    self.processes.sort(key=lambda x: x.duration)  #organiza por duration time

    #calcula os tempos previamente dependendo do tempo de duraçao
    for process in self.processes:
      if self.counter < process.arrivalTime:  #necessita esperar
        self.counter += process.arrivalTime - self.counter
      process.waitingTime = self.counter - process.arrivalTime
      process.responseTime = self.counter - process.arrivalTime
      process.turnAround = self.counter + process.duration - process.arrivalTime
      process.processTime = process.turnAround - process.waitingTime
      self.DoProcess(process)

      self.counter += process.duration

    self.processes.sort(key=lambda x: x.arrivalTime)

  def resetPar(self):
    self.counter = 0
    for process in self.processes:
      process.remainTime = process.duration
      process.waitingTime = 0
      process.responseTime = 0
      process.processTime = 0
      process.turnAround = 0

  def printDurations(self, string):
    print(f"Duration for {string}")
    for i in range(len(self.processes)):
      print(f"-----Process {i+1}-----")
      print("  Waiting Time:", self.processes[i].waitingTime)
      print("  Response Time:", self.processes[i].responseTime)
      print("  Processing Time:", self.processes[i].processTime)
      print("  TurnAround Time:", self.processes[i].turnAround)
      print()
    print("----------------------------------")

  def DoProcess(self, process):
    #nao implementado
    pass


def main():
  allProcess = [
      Process(arrivalTime=0, duration=24),
      Process(arrivalTime=1, duration=3),
      Process(arrivalTime=2, duration=3),
  ]

  Scheduler = ProcessSchedule(allProcess)
  Scheduler.FCFS()
  Scheduler.printDurations("FCFS")

  #resetando parametros
  Scheduler.resetPar()

  Scheduler.RR(3)
  Scheduler.printDurations("RR")

  #resetando parametros
  Scheduler.resetPar()

  Scheduler.SJF()
  Scheduler.printDurations("SJF")


if __name__ == "__main__":
  main()
