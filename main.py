import argparse
import sys
import pcfgen.data
import pcfgen.model

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='''
This program use PCFG (Probabilistic Context Free Grammar), has three funtions:
1. Learn from a password list and generate a model;
2. Generate a password attack dictionary from a model;
3. Test password attack dictionary on a password set.
''')
    parser.add_argument('action', choices=[
                        'train', 'gen', 'test'], help='''Specify the behavior of the program. 
"train": learn model parameters from password set;
"gen": generate attack dictionary based on model;
"test": test the attack dictionary on a password set.''')
    parser.add_argument(
        '-d', '--data', choices=['csdn', 'yahoo'], help='Specify the type of password set (csdn/yahoo).')
    parser.add_argument(
        '-o', '--output', help='Specify the path to the output model (train) or dictionary (generate).')
    parser.add_argument('-l', '--length', type=int,
                        default=5000, help='Specify the length of the attack dictionary. Default 5000.')
    # args.add_argument('-w', '--with-prob', help='指定生成字典时写入概率值。')
    parser.add_argument(
        '-p', '--pwdict', help='Specify the path to the password dictionary to be tested.')
    parser.add_argument(
        'infile', help='Specify the path to input file (train: password set; gen: model file; test: password set to test on).')
    args = parser.parse_args()

    if args.action == 'train':
        if args.output == None:
            print('Missing -o/--output: must specify the output file path when training')
            sys.exit(0)
        if args.data == None:
            print('Missing -d/--data: must specify the input data type (csdn/yahoo)')
            sys.exit(0)
        elif args.data == 'csdn':
            d = pcfgen.data.CSDN(args.infile)
        elif args.data == 'yahoo':
            d = pcfgen.data.Yahoo(args.infile)

        m = pcfgen.model.Model()
        m.fit(d)
        m.export(args.output)

    elif args.action == 'gen':
        if args.length <= 0:
            print('Error -l/--length: must be positive integer!')
            sys.exit(0)
        if args.output == None:
            print('Missing -o/--output: must specify the output file path when training')
            sys.exit(0)

        m = pcfgen.model.Model()
        m.load_model(args.infile)
        m.generate(args.output, args.length)

    elif args.action == 'test':
        if args.data == None:
            print('Missing -d/--data: must specify the input data type (csdn/yahoo)!')
            sys.exit(0)
        elif args.data == 'csdn':
            testset = list(pcfgen.data.CSDN(args.infile))
        elif args.data == 'yahoo':
            testset = list(pcfgen.data.Yahoo(args.infile))

        if args.pwdict == None:
            print('Missing -p/--pwdict: must specify the path of passord dictionary!')
            sys.exit(0)

        pwdict = pcfgen.data.Pwdlist(args.pwdict)
        pwdict.test(testset)
