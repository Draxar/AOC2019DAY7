from itertools import permutations

#inputProgram = list(map(int,input().split(",")))
#hardcoded input
inputProgram = [3,8,1001,8,10,8,105,1,0,0,21,46,67,76,101,118,199,280,361,442,99999,3,9,1002,9,4,9,1001,9,2,9,102,3,9,9,101,3,9,9,102,2,9,9,4,9,99,3,9,1001,9,3,9,102,2,9,9,1001,9,2,9,1002,9,3,9,4,9,99,3,9,101,3,9,9,4,9,99,3,9,1001,9,2,9,1002,9,5,9,101,5,9,9,1002,9,4,9,101,5,9,9,4,9,99,3,9,102,2,9,9,1001,9,5,9,102,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,101,1,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,1,9,9,4,9,3,9,102,2,9,9,4,9,3,9,1001,9,1,9,4,9,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,99,3,9,1002,9,2,9,4,9,3,9,1001,9,1,9,4,9,3,9,101,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,1001,9,2,9,4,9,99,3,9,102,2,9,9,4,9,3,9,102,2,9,9,4,9,3,9,101,2,9,9,4,9,3,9,101,1,9,9,4,9,3,9,101,2,9,9,4,9,3,9,1001,9,2,9,4,9,3,9,1001,9,2,9,4,9,3,9,101,2,9,9,4,9,3,9,1002,9,2,9,4,9,3,9,101,2,9,9,4,9,99]

class compu:
  def __init__(self, prog, inp):
    self.program = list(prog)
    self.inputBuffer = list(inp)
    self.outputBuffer = list()
    self.state = 1 #1=new, 2=ended, 3=paused
    self.itr = 0

  def addInput(self, inp):
    self.inputBuffer.extend(inp)

  def parseCode(self, code):
    p3 = int(code / 10000)
    code = code % 10000
    p2 = int(code / 1000)
    code = code % 1000
    p1 = int(code / 100)
    code = code % 100
    return p1, p2, p3, code

  #parse and process opcode
  def processCode(self, itr):
    code = self.program[itr]
    p1, p2, p3, code = self.parseCode(code)
    if code == 99:
      return "quit"

    # process code
    # 1 parameter
    if p1 == 1:
      ind1 = itr+1
    else:
      ind1 = self.program[itr+1]
    if code == 3:
      if not self.inputBuffer:
        return "pause"
      self.program[ind1] = self.inputBuffer.pop(0)
      return 2
    if code == 4:
      self.outputBuffer.append(self.program[ind1])
      return 2
    # 2 parameters  
    if p2 == 1:
      ind2 = itr+2
    else:
      ind2 = self.program[itr+2]
    if code == 5:
      if self.program[ind1] != 0:
        return self.program[ind2] - itr
      else:
        return 3
    if code == 6:
      if self.program[ind1] == 0:
        return self.program[ind2] - itr
      else:
        return 3 
    # 3 parameters  
    if p3 == 1:
      ind3 = itr+3
    else:
      ind3 = self.program[itr+3]
    if code == 1:
      self.program[ind3] = self.program[ind1] + self.program[ind2]
      return 4
    if code == 2:
      self.program[ind3] = self.program[ind1] * self.program[ind2]
      return 4
    if code == 7:
      if self.program[ind1] < self.program[ind2]:
        self.program[ind3] = 1
        return 4
      self.program[ind3] = 0
      return 4
    if code == 8:
      if self.program[ind1] == self.program[ind2]:
        self.program[ind3] = 1
        return 4
      self.program[ind3] = 0
      return 4

    print("BAD CODE:")
    print(str(code))
    return "quit"

  # prepere and process program
  def ProcessProgram(self):
    #prep program
    move = 0
    process = True
    #process program
    while process:
      move = self.processCode(self.itr)
      if move == "quit":
        self.state = 2
        self.itr = 0
        process = False
      elif move == "pause":
        self.state = 3
        process = False
      else :
        self.itr += move
    return self.state, self.outputBuffer


# main
answer = 0
phase_inp = [5,6,7,8,9]
# try all permutations of phases
perm = permutations(phase_inp) 
for i in list(perm): 
  phase = list(i)
  buf = list()
  computers = list()
  ret = [0]
  iter = 0
  for i in range(5):
    buf.append(phase.pop())
    buf.append(ret.pop())
    com = compu(inputProgram,buf)
    state, ret = com.ProcessProgram()
    computers.append(com)
    buf.clear()
  finished = 0
  mod = 0
  while finished < 5:
    computers[mod%5].addInput(ret)
    ret.clear()
    state, ret = computers[mod%5].ProcessProgram()
    mod+=1
    if state == 2:
      finished += 1

  tempa = ret.pop()
  print(tempa)
  if answer < tempa:
    answer = tempa
  

print("--ANSWER--")
print(answer)
print("----------")