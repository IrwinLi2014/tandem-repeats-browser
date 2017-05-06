# tandem-repeats-browser
A tandem repeats finder designed for human genome, implemented by Chuchu Ding and Dejia Tang.


# Dependencies
Please be sure to install the following dependencies, before running the program and testing it on either command line or its web user interface:
* sudo pip install web.py
* sudo pip install numpy
* sudo pip install biopython


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

When this line is run, the default output file will be stored in output.csv, with each line representing the indices of one tandem repeat.

> repeat start index, repeat pattern end index, whole repeat end index



# Video Demo
A recorded demo of this program's web user interface can be found at: <https://youtu.be/SjnhRwCYq88>.

