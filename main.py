import random as rnd

def plus_state_measure():
    outcomes = [0,1]
    return rnd.choice(outcomes)


if __name__ == '__main__':
    result = plus_state_measure()
    print(result)

    print('done!')
