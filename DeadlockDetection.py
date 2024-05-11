#processes = ["P0", "P1", "P2", "P3", "P4"]
#qntProc = len(processes)    #quantity of processess
#qntRes = 3                  #quantity of resources

#availableRes = [3, 3, 2]    #available resources
#maxRes = [[7, 5, 3],
#         [3, 2, 2],
#         [9, 0, 2],
#         [2, 2, 2],
#         [4, 3, 3]]    #maximum resource that each process can request

#allocRes = [[0, 1, 0],
#           [2, 0, 0],
#           [3, 0, 2],
#           [2, 1, 1],
#           [0, 0, 2]]  #resorces that each process is currently allocated

class Deadlock:
  def __init__(self, qntProc, qntRes):
    self.qntProc = qntProc  #quantity of resources
    self.qntRes = qntRes    #quantity of resources

  def inciciateMatrixNeed(self):
    need = []
    for _ in range(self.qntProc):
      list = []
      for _ in range(self.qntRes):
        list.append(0)
      need.append(list)
      
    return need
    
  def makeNeed(self, maxRes, allocRes):
    need = self.inciciateMatrixNeed()
    for i in range(self.qntProc):
      for f in range(self.qntRes):
        need[i][f] = maxRes[i][f] - allocRes[i][f]
        
    return need

  def printProcesses(self, processes, safeSeq):
    for i in range(self.qntProc):
      print(f"{processes[safeSeq[i]]}")

  
  def BankerAlgorithm(self, processes, availableRes, allocRes, need):
    #1
    fim = [0] * self.qntProc    # Vetor Fim
    disp = [0] * self.qntRes    #vetor disponivel
    #False = 0 e True != 0
    
    for i in range(self.qntRes):
      disp[i] = availableRes[i]
    #
    #2
    count = 0
    sequence = []
    while count < self.qntProc:
      found = False
      
      for P in range(self.qntProc):    #indice
        if fim[P] == 0:  #(a)
          for f in range(self.qntRes):
            if need[P][f] > disp[f]: # (b)
              break
          if f == self.qntRes - 1:#checa se todos os recursos foram chamados
            #3 Atualizar recursos disponíveis
            for j in range(self.qntRes):
              disp[j] += allocRes[P][j]# Disp[r] = Disp[r] + Alocação[p,r]
            sequence.append(P)
            count += 1
            fim[P] += 1 # Fim[p] = true
            found = True
      if not found:  #4
        print("System is not in safe state")
        return False, sequence
    
    return True, sequence

  def checkDeadlock(self, available, allocation, need):
    fim = [False] * self.qntProc  #vetor fim
    worker = list(available)      #vetor trabalho = vetor disponivel

    # Inicialização nomeando se o vetor fim é True ou False para todo recurso
    for i in range(self.qntProc):
      if all(allocation[i][j] == 0 for j in range(self.qntRes)):
        fim[i] = True
      else:
        fim[i] = False

    while True:
      flag = 0

      #procurar um processo que não está em fim e que pode ser executado
      for i in range(self.qntProc):
        if fim[i] is False and all(need[i][j] <= worker[j] for j in range(self.qntRes)):  #se nunca encontrar o P ele nunca entrara no if
          # Atualiza work conforme o processo i pode prosseguir
          for j in range(self.qntRes):
            worker[j] += allocation[i][j]
          fim[i] = True
          flag += 1

      if flag == 0:
        break

    # Passo 4: verificar se algum processo está em deadlock
    if any(f is False for f in fim):
      return True  # Deadlock detectado
    else:
      return False  # Sem deadlock

def main():
  processes = ["P0", "P1", "P2", "P3", "P4"]
  qntProc = len(processes)    #quantity of processess
  qntRes = 3                  #quantity of resources
  
  availableRes = [3, 3, 2]    #available resources
  maxRes = [[7, 5, 3],
           [3, 2, 2],
           [9, 0, 2],
           [2, 2, 2],
           [4, 3, 3]]    #maximum resource that each process can request
  
  allocRes = [[0, 1, 0],
             [2, 0, 0],
             [3, 0, 2],
             [2, 1, 1],
             [0, 0, 2]]  #resorces that each process is currently allocated

  deadlock = Deadlock(qntProc, qntRes)
  need = deadlock.makeNeed(maxRes, allocRes)

  flag = deadlock.checkDeadlock(availableRes, allocRes, need)
  if flag is True:
    print("The processes have deadlock.")
  else:
    print("The processes don't have deadlock.")

  print()
  
  flag, sequence = deadlock.BankerAlgorithm(processes, availableRes, allocRes, need)
  if flag is True:
    print("The processesses don't have deadlock in the sequence: ", sequence)
    deadlock.printProcesses(processes, sequence)
  else:
    print("The processesses have deadlock")


if __name__ == "__main__":
  main()
