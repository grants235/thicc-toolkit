from cli.repl import Repl
import argparse 

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--project", help = "Provide an existing project folder or specify the name of a new one")

    args = parser.parse_args()

    repl = Repl(project_arg=args.project, threads=10)
    repl.run()
    

if __name__ == "__main__":
    main()