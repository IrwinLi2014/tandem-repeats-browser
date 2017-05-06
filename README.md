# tandem-repeats-browser
A tandem repeats finder designed for human genome, implemented by Chuchu Ding and Dejia Tang.


# Dependencies
Please be sure to install the following dependencies, before running the program and testing it on either command line or its web user interface:
* sudo pip install web.py
* sudo pip install numpy
* sudo pip install biopython
> Replace pip with pip2 or pip3 if the program fails after running the above lines.

A powerful machine is prefered. For example, we used Amazon Web Services (<https://aws.amazon.com/free/>) for testing.


# Usage

## This program runs on Python 2.  
Running the following command on the command line displays the help information for its command line usage:

> python2 tandem.py --help
>
>>usage: tandem.py [-h] [-m MISMATCH] [-w WINDOW] [-s SEQUENCE] [-a ALPHABET] [-i INPUT] [-o OUTPUT] [-b BOND]
>
>>Finding tandem repeats.
>
>>optional arguments:
>
>>  -h, --help            show this help message and exit
>
>>  -m MISMATCH, --mismatch MISMATCH
>
>>                        Mismatch tolerance in percentage.
>>
>>  -w WINDOW, --window WINDOW
>>
>>                        Window size.
>>
>>  -s SEQUENCE, --sequence SEQUENCE
>>
>>                        sequence to be searched
>>
>>  -a ALPHABET, --alphabet ALPHABET
>>
>>                        sequence to be searched
>>
>>  -i INPUT, --input INPUT
>>
>>                        input file
>>
>>  -o OUTPUT, --output OUTPUT
>>
>>                        output file
>>
>>  -b BOND, --bond BOND  lower boundary

A sample usage of the command line version may be:

> python2 tandem.py -m 0 -w 5 -s ATCGCGTTAAAAAGAGGGGTATATATAAATGACCTA

or

> python2 tandem.py -m 5 -w 1000 -a ATCG -i input.fna

When no output file is specified, by default the output will be stored in output.csv, with each line representing the indices of one tandem repeat.

> repeat start index, repeat pattern end index, whole repeat end index

## A more recommended way is to test through its web user interface, which dynamically displays all found repeats after storing their indices.

Launch the server locally using the following:

> python2 server.py

The default port is: <http://0.0.0.0:8080/>


# Project Composition

In this package:

tandem.py        
> The main algorithm to find tandem repeats, and store their indices into an output file.

server.py        
> The server to launch the program's web interface.

showrepeats_2.py    
> Reads the indices of found repeats stored in out.csv, converts them into readable repeats, and displays them dynamically on the web interface.  
This functionality only supports the default output filename (out.csv) currently.

input.fna        
> A portion of the encoding of chromosome 9 that can be used as an input sequence file, provided for testing purposes.

More FNA files of human genome sequence can be downloaded at Human Genome Resources at NCBI: <https://www.ncbi.nlm.nih.gov/projects/genome/guide/human/>.



# Video Demo
A recorded demo of this program's web user interface can be found at: <https://youtu.be/SjnhRwCYq88>.

