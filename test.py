import argparse

def main():
    parser = argparse.ArgumentParser(description="Command-line tool for video steganography")
    parser.add_argument('-es','--encode-string',metavar='S',type=str,help='string for encryption')
    parser.add_argument('-s','--source',metavar='U',type=str,help='source for video path')
    parser.add_argument('-d','--destination',metavar='D',type=str,help='destination for video path')
    parser.add_argument('--encryption',action='store_true',help="for encryption")
    arg_dict = parsed_dict(parser)
    
    if arg_dict['encryption']:
        #Encryption
        if arg_dict['encode_string'] is None:
            parser.print_usage()
            parser.exit(status=1,message="encode string is required in encryption\n")
        elif arg_dict['source'] is None:
            parser.print_usage()
            parser.exit(status=1,message="source should be specified for encryption\n")
    else:
        #Decryption
        if arg_dict['encode_string'] is not None or arg_dict['destination'] is not None:
            parser.print_usage()
            parser.exit(status=1,message="-es / -d is not required for decryption\n")
        elif arg_dict['source'] is None:
            parser.print_usage()
            parser.exit(status=1,message="-s is required for decryption\n")            

def parsed_dict(parser):
    return parser.parse_args().__dict__


if __name__ == "__main__":
    main()