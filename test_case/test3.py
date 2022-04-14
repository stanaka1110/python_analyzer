import sys

def main():
    for idx, line in enumerate(sys.stdin):
        a, b = map(int, line.split())
        print(len(str(a+b)))
    l = [2, 3, 5, 6]
    for i in l:
        print(i)

if __name__ == "__main__" :
    main()