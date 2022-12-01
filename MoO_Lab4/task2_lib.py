from random import uniform
import numpy as np
import pandas as pd

class Cords(np.ndarray):
    def __str__(self) -> str:
        cords_str_list = [f"x{i} = {self.__getitem__(i)}" for i in range(self.size)]
        return '[' + ','.join(cords_str_list) + ']'

def get_str_cords(cords):
    cords_str_list = [f"x{i} = {cords[i]}" for i in range(len(cords))]
    return '[' + ','.join(cords_str_list) + ']'

class FuncMinFinder:
    print_tries = False

    def __init__(self, func) -> None:
        self.func = func        

    def return_on_an_unsuccessful_step(self, x0 : np.ndarray, betta=0.5, M=10, t0=10, R=0.1, N=10) -> np.ndarray:
        cords_num = len(x0)
        
        k = 0
        j = 1 
        xk = x0
        tk = t0
        is_k_reached_N = False
        while not is_k_reached_N:
            print(f"Итерация {k}")
            print(f"\tx{k}: {get_str_cords(xk)}")   
            f_xk = self.func(xk)      
            print(f"\tf(x{k}): {f_xk}")   
            print(f"\tt{k}: {tk}\n")   
            while True:
                if self.print_tries:
                    print(f"\tПопытка {j}")
                y = 0                
                while True:
                    rand_vec = np.array([uniform(-1, 1) for _ in range(cords_num)])
                    vec_norm = np.linalg.norm(rand_vec, ord=2)
                    y : np.ndarray = xk + tk * (rand_vec / vec_norm)
                    if ((y > 0).all()):
                        break
                if self.print_tries:
                    print(f"\t\ty: {get_str_cords(y)}")
                f_y = self.func(y)
                if self.print_tries:
                    print(f"\t\tf(y): {f_y}")
                is_new_f_less = f_y < f_xk
                inequality_symb = '<' if is_new_f_less else '>='
                if self.print_tries:
                    print(f"\t\tf(y) {inequality_symb} f(x{k}) ({f_y} {inequality_symb} {f_xk})")
                if (is_new_f_less):
                    xk = y
                    k += 1
                    is_k_reached_N = k == N
                    j = 1                        
                    break
                if j < M:
                    j += 1
                    continue
                if self.print_tries:
                    print("\n\t\tj = M")
                if tk <= R:
                    if self.print_tries:
                        print(f"\t\t{k} <= R ({tk} <= {R})")
                        print("\t\tОстановка процесса оптимизации.")
                    is_k_reached_N = True
                    break
                tk *= betta
                if self.print_tries:
                    print (f"\t\tt{k} = t{k} * betta = {tk}")                
                    print(f"\t\tНачало новых попыток итерации {k}.\n")
                j = 1

        print(f"x_min = {get_str_cords(xk)}")
        print(f"f_min = {f_xk}")
        return xk