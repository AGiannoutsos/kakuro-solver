import time
import csp
import search
import copy
import sys

# Definition of the problem
class Kakuro(csp.CSP):

    def __init__(self, puzzle):

        rows = len(puzzle)
        cols = len(puzzle[0])
        self.rows = rows
        self.cols = cols
        self.puzzleVals = copy.deepcopy(puzzle)
      
        puzzleVar = [[ 0 for i in range(cols)] for i in range(rows)]

        blacks = []
        info = []
        variables = []
        domains = {}
        neighbors = {}
        conArrays = {}

        #for variables
        for i in range(rows):
            for j in range(cols):
                puzzleVar[i][j] = str(i)+'_'+str(j)
                if puzzle[i][j] == '*':
                    blacks.append(str(i)+'_'+str(j))
                elif puzzle[i][j] == '_':
                    variables.append(str(i)+'_'+str(j))
                    self.puzzleVals[i][j] = 0
                else:
                    info.append(str(i)+'_'+str(j))
        
        # for domain
        d = [i for i in range(1,10)]
        for var in variables:
            domains[var] = d.copy()
            neighbors[var] = []
        
        # for neighbors
        for i in range(rows):
            for j in range(cols):
                if puzzleVar[i][j] in variables:
                    # for Rows
                    for row in reversed(puzzleVar[i][:j]):
                        if (row in blacks) or (row in info):
                            break
                        else:
                            if row != puzzleVar[i][j]:
                                neighbors[puzzleVar[i][j]].append(row)
                    for row in puzzleVar[i][j:]:
                        if (row in blacks) or (row in info):
                            break
                        else:
                            if row != puzzleVar[i][j]:
                                neighbors[puzzleVar[i][j]].append(row)

                    # for Cols
                    for col in reversed([puz[j] for k,puz in enumerate(puzzleVar) if k<i]):
                        if (col in blacks) or (col in info):
                            break
                        else:
                            if col != puzzleVar[i][j]:
                                neighbors[puzzleVar[i][j]].append(col)
                    for col in [puz[j] for k,puz in enumerate(puzzleVar) if k>i]:
                        if (col in blacks) or (col in info):
                            break
                        else:
                            if col != puzzleVar[i][j]:
                                neighbors[puzzleVar[i][j]].append(col)
                
        # for constraints info
        # Get the array of variables for each constraint
        for i in range(rows):
            for j in range(cols):
                if len(puzzle[i][j]) == 2:
                    if puzzle[i][j][1] != '':
                        k = j+1
                        tempInfo = []
                        while(puzzle[i][k] == '_'):
                            tempInfo.append(puzzleVar[i][k])
                            k += 1
                            if k> cols-1:
                                break
                        conArrays[str(puzzle[i][j][1])+'_'+puzzleVar[i][j]+'_O']   = tempInfo
                        del tempInfo

                    if puzzle[i][j][0] != '':
                        k = i+1
                        tempInfo = []
                        while(puzzle[k][j] == '_'):
                            tempInfo.append(puzzleVar[k][j])
                            k += 1
                            if k> rows-1:
                                break
                        conArrays[str(puzzle[i][j][0])+'_'+puzzleVar[i][j]+'_V']   = tempInfo
                        del tempInfo         

        self.puzzle = puzzle
        self.conArrays = conArrays
        self.puzzleVar = puzzleVar
        self.neighbors = neighbors
        self.variables = variables
        self.domains   = domains

        super().__init__(variables, domains, neighbors,self.kakuroConstraints)

    # find the needed sum
    def getSumCon(self,con):
        pos = con.find('_')
        return int(con[:pos])

    #get variables from constrain and convert them to values
    #use the already assigned values from self.currAssignments
    def varsToVals(self,con,A,B):
        lis = []
        for var in con:
            #exclude already A or B because they will change
            if (var in self.currAssignments):
                if not (var == A or var == B):
                    lis.append(self.currAssignments[var])            
        return lis

            
    def kakuroConstraints(self,A,a,B,b):
        # find all conflicts
        # get the same conflict of A and B
        cons = set()
        cons.update([con for con, conArr in self.conArrays.items() if (A in conArr) and (B in conArr)])
        con = cons.pop()
        #get array of variables
        conArray = self.conArrays[con]
        lis = []

        # if neighbors and equal then false
        if a == b:
            return False
     
        # Calculate the sum
        #if length of lis is full of values then in means
        #that every variable is assigned then the sum must be equal to constrain
        lis = self.varsToVals(conArray,A,B)
        if len(lis) + 2 == len(conArray):
            if sum(lis) + a + b == self.getSumCon(con):
                return True
            else:
                return False

        # if length = 2 then the sum must be the constrain
        elif len(conArray) == 2:
            if a + b == self.getSumCon(con):
                return True
            else:
                return False 
                
        #else if not then the sum can be less than the constrain
        else:
            if sum(lis) + a + b < self.getSumCon(con):
                return True
            else:
                return False  


    def display(self, assignment=None):
        for i, line in enumerate(self.puzzle):
            puzzle = ""
            for j, element in enumerate(line):
                if element == '*':
                    puzzle += "[*]\t"
                elif element == '_':
                    var1 = str(i)
                    if len(var1) == 1:
                        var1 =  var1
                    var2 = str(j)
                    if len(var2) == 1:
                        var2 =  var2
                    var = var1+ '_' +var2
                    if assignment is not None:
                        if isinstance(assignment[var], set) and len(assignment[var]) is 1:
                            puzzle += "[" + str(first(assignment[var])) + "]\t"
                        elif isinstance(assignment[var], int):
                            puzzle += "[" + str(assignment[var]) + "]\t"
                        else:
                            puzzle += "[_]\t"
                    else:
                        puzzle += "[_]\t"
                else:
                    puzzle += str(element[0]) + "\\" + str(element[1]) + "\t"
            print(puzzle)                    




if __name__ == "__main__":

    #kakuro[1,2,3,4]
    #[easy, easy, hard, very hard]

    kakuroProblemNum = 0
    kakuro = csp.kakuro1
    try:
        kakuroProblemNum = int(sys.argv[-1].split("kakuro")[-1])
    except:
        print("Wrong input \nrun simple kakuro1")
    
    if kakuroProblemNum == 1:
        kakuro = csp.kakuro1
    elif kakuroProblemNum == 2:
        kakuro = csp.kakuro2
    elif kakuroProblemNum == 3:
        kakuro = csp.kakuro3
    elif kakuroProblemNum == 4:
        kakuro = csp.kakuro4
    else:
        kakuro = csp.kakuro1

    
    ############### Backtracking ###############
    problem = Kakuro(kakuro)
    start = time.time()
    BT_results = csp.backtracking_search(problem)
    end = time.time()

    problem.display(BT_results)
    print ("BT time: " + str(end-start) + " assigns: " + str(problem.nassigns)+"\n\n")


    # ############### Backtracking + MRV ###############
    # problem = Kakuro(kakuro)
    # start = time.time()
    # BT_MRV_results = csp.backtracking_search(problem, select_unassigned_variable=csp.mrv)
    # end = time.time()

    # problem.display(BT_MRV_results)
    # print ("Backtracking + MRV time: " + str(end-start) + " assigns: " + str(problem.nassigns)+"\n\n")


    ############### Forward check ###############
    problem = Kakuro(kakuro)
    start = time.time()
    FC_results = csp.backtracking_search(problem, inference=csp.forward_checking)
    end = time.time()

    problem.display(FC_results)
    print ("FC time: " + str(end-start) + " assigns: " + str(problem.nassigns)+"\n\n")


    ############### Forward check + MRV ###############
    problem = Kakuro(kakuro)
    start = time.time()
    FC_MRV_results = csp.backtracking_search(problem, select_unassigned_variable=csp.mrv, inference=csp.forward_checking)
    end = time.time()

    problem.display(FC_MRV_results)
    print ("FC + MRV time: " + str(end-start) + " assigns: " + str(problem.nassigns)+"\n\n")


    ############### MAC ###############
    problem = Kakuro(kakuro)
    start = time.time()
    MAC_results = csp.backtracking_search(problem, inference=csp.mac)
    end = time.time()

    problem.display(MAC_results)
    print ("MAC time: " + str(end-start) + " assigns: " + str(problem.nassigns)+"\n\n")


    # ############### MAC + MRV ###############
    # problem = Kakuro(kakuro)
    # start = time.time()
    # MAC_MRV_results = csp.backtracking_search(problem, select_unassigned_variable=csp.mrv, inference=csp.mac)
    # end = time.time()

    # problem.display(MAC_MRV_results)
    # print ("MAC + MRV time: " + str(end-start) + " assigns: " + str(problem.nassigns)+"\n\n")