# Testing

I created unit tests for all functions with simple inputs and outputs that I calculated to be right by hand. The unit tests are made with native Python unittest library. The inputs are given as text or binary files and the outputs can be found from test_huffman.py and test_lzw.py. I also compared the speed and efficiency of both Huffman and LZW. The unit tests can be run with the command "python3 -m unittest".

## Huffman vs LZW

As we can see from the graph down below, LZW seems to be more efficient when file size increases. This is natural because LZW works by finding bigger and bigger patterns from the given text. The more there is text, the more these patterns will emerge.

![Comparison of the compression efficiency of Huffman and LZW in graphical form.](./huffmanvslzwlight.svg#gh-light-mode-only)
![Comparison of the compression efficiency of Huffman and LZW in graphical form.](./huffmanvslzwdark.svg#gh-dark-mode-only)

### Huffman

| File | Size (Bytes) | Compressed size (Bytes) | Compressing time (s) | Decompressing time (s) |
| --------- | ---- | ---- | ----- | ---- |
| test0.txt | 10 | 22 | 0.001 | 0.001 |
| test1.txt | 20 | 41 | 0.0006 | 0.0003 |
| test2.txt | 40 | 65 | 0.0006 | 0.0005 |
| test3.txt | 80 | 112 | 0.0008 | 0.0006 |
| test4.txt | 160 | 165 | 0.0009 | 0.0011 |
| test5.txt | 320 | 262 | 0.0012 | 0.0013 |
| test6.txt | 640 | 463 | 0.0012 | 0.0028 |
| test7.txt | 1280 | 952 | 0.0015 | 0.0055 |
| test8.txt | 2560 | 1726 | 0.0017 | 0.0114 |
| test9.txt | 5120 | 3294 | 0.0027 | 0.0201 |
| test10.txt | 10240 | 6234 | 0.0052 | 0.0434 |
| test11.txt | 20480 | 11990 | 0.0083 | 0.0724 |
| test12.txt | 40960 | 23403 | 0.018 | 0.1426 |
| test13.txt | 81920 | 46218 | 0.0306 | 0.2644 |
| test14.txt | 163840 | 94579 | 0.0576 | 0.5186 |
| test15.txt | 327680 | 193421 | 0.1067 | 1.0261 |
| test16.txt | 655360 | 389994 | 0.2186 | 2.1369 |
| test17.txt | 1310720 | 780463 | 0.4209 | 4.3987 |
| test18.txt | 2621440 | 1564673 | 0.874 | 8.8336 |
| test19.txt | 5242880 | 3128172 | 1.7089 | 17.4349 |

### LZW

| File | Size (Bytes) | Compressed size (Bytes) | Compressing time (s) | Decompressing time (s) |
| --------- | ---- | ---- | ----- | ---- |
| test0.txt | 10 | 18 | 0.0167 | 0.0132 |
| test1.txt | 20 | 40 | 0.0137 | 0.0102 |
| test2.txt | 40 | 78 | 0.0127 | 0.0092 |
| test3.txt | 80 | 157 | 0.012 | 0.01 |
| test4.txt | 160 | 267 | 0.0126 | 0.01 |
| test5.txt | 320 | 480 | 0.0115 | 0.0098 |
| test6.txt | 640 | 826 | 0.0119 | 0.0096 |
| test7.txt | 1280 | 1559 | 0.0132 | 0.0102 |
| test8.txt | 2560 | 2658 | 0.0149 | 0.0124 |
| test9.txt | 5120 | 4778 | 0.0162 | 0.0141 |
| test10.txt | 10240 | 8331 | 0.0198 | 0.0173 |
| test11.txt | 20480 | 14592 | 0.0263 | 0.0313 |
| test12.txt | 40960 | 25644 | 0.0431 | 0.0347 |
| test13.txt | 81920 | 45559 | 0.0616 | 0.056 |
| test14.txt | 163840 | 84188 | 0.1029 | 0.0951 |
| test15.txt | 327680 | 154534 | 0.1768 | 0.1657 |
| test16.txt | 655360 | 288625 | 0.3376 | 0.3094 |
| test17.txt | 1310720 | 546814 | 0.6812 | 0.6564 |
| test18.txt | 2621440 | 1040242 | 1.4111 | 1.0778 |
| test19.txt | 5242880 | 2006879 | 2.8852 | 2.0549 |

## Code coverage report

![Screenshot of code coverage report generated with Coverage](./coverage.png)