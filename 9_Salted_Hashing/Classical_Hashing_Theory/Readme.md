# Hashing 
## Intro 
 1) a cryptographic hash function is a mathematical algorithm that maps data of arbitrary size (message) to a bit array of a fixed size (message digest or hash)
 2) All operations are public - such as the h(x) hash-function
 3) There are no private keys here
 4) It is deterministic and random (pseudo-random) 

h: {0,1}*  ---> {0,1}^d  
MD5  - d is 128 bits
SHA1 - d is 160 bits 
SHA2 - d is 256 bits 

## Properties of Hashing

### PRE-IMAGE RESISTANCE: 
it is exponentially hard (computationally infeasible) to determine the m message from the h(m) message digest

### SECOND PRE-IMAGE RESISTANCE -
if m1 is given then it is infeasible to find m2, such that h(m1) = h(m2) so the hashes are the same


### COLLISION RESISTANCE
it is infeasible to find any m1, and m2, messages such that h(m1) = h(m2). It is easier to break collision resistance than the second pre-image resistance.


1) deterministic: it means that if we apply to same hash-function (SHA256) on the exact same input then the output must be the same

2) one-way: it is easy to generate the hash with the given hashing algorithm but on the other hand it is extremely hard (time-consuming) to restore the original input
~ it is like a trap-door function

3) collision-free: there are no collisions in SHA256 (ok there are but with extremely low probability)
It means that no two different inputs share the same output hash
~ and this is good: we want to make these hashes unique, this is how we identify a block in the blockchain

4) avalanche effect: a little change in the input results in a completely different output hash
~ otherwise a cryptoanalyst can make predictions about the input
based on the output exclusively

## Birthday Paradox 

#### Let us assume N people in a room . What is the probability that nobody shares a birthday ?

= 1 * 364/365 * 363/365 * 362/365 ...... (365 - (N-1))/365

=  (1/365) ^ N Product (i=0 to N-1) of (365 -i)

#### Probability that atleast two people share the birthday 

= 1 - (1 * 364/365 * 363/365 * 362/365 ...... (365 - (N-1))/365)

So we assume that at least 2 people share the same birthday with 50% probability

0.5 = 1 - (1/365) ^ N Product (i=0 to N-1) of (365 -i)
N = 23

So for 128 bit lonh hash, there are 2^ 128 possible hashes,
After applying birthday paradox, we end up with 2^64 