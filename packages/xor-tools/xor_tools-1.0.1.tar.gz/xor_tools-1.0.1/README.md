# XOR tools

## Description

A set of tools for XOR encryption/decryption/key recovery (based on known plaintext). 

## Install

```
git clone https://github.com/lukaskuzmiak/xor_tools.git
python setup.py install
```

## Example Usage

First, we create example XOR encrypted `samples/binary_pe32` file:

```bash
xor_encrypt_file -f samples/binary_pe32 -o encrypted.file -k "secret"
```

You can also enter non-ascii keys as `-k "\xaa\xbb\xcc\xdd"`.

To recover the secret key `secret`, the second tool `xor_key_recovery` is used. We expect a PE binary to contain a phrase `This program cannot be run in DOS`. We don't know the key length, but after few tries with consecutive `-n 1`, `-n 2`, `-n 3` ... we finally try `-n 6`:

```bash
xor_key_recovery -f encrypted.file -o decrypted.file -p "This program cannot be run in DOS" -n 6

[+] Found plaintext at position: 78
[*] Key found: 736563726574
[+] Saving decrypted file to: decrypted.file
```

You can also enter non-ascii plaintext as `-p "\xaa\xbb\xcc\xdd"`.

## How it works

It's quite easy to understand on example but it's not a formal proof though (or maybe because of it).

### Prepare template

First we need part of plaintext before being encrypted. Anything slightly longer than key length would be sufficient but to avoid false positives twice as long plaintext is preferred. We could in many cases guess it (like common phrases, strings etc.).

```
P[] = "This program cannot be run in DOS"
```

The other thing we will need is secret key length -- we could also guess it or iterate over possible key lengths (n=3, n=4, n=5 ...).

```
keylength = 6
```

Now, if we xor symbols from plaintext that are keylength apart, we receive:

```
T[1] = P[i] XOR P[i+k_len]
```

We build template that way of first part of the string XORed with another symbols one keylength apart.

### Surprising XOR cipher characteristics

Because in ciphertext symbols one keylength apart are XORed with the same secret key symbol we get:

```
C[i] = P[i] XOR Key[i]
C[i+k_len] = P[i+k_len] XOR Key[i]
```

If we XOR these two, we surprisingly (because of XOR characteristics) receive something independent from secret key used:

```
C[i] XOR C[i+k_len] = ( P[i] XOR Key[i] ) XOR ( P[i+k_len] XOR Key[i] ) =
                    = ( P[i] XOR P[i+k_len] ) XOR ( Key[i] XOR Key[i] ) =
                    = P[i] XOR P[i+k_len]
```

This is exactly the same, as our template and it's independent from secret key.

### Final blow

Now, when we do this for whole ciphertext (eg. encrypted file) we look for our template.
This way, we've found place in ciphertext where our encrypted string is and w know what it's plaintext version is.

From this place, it's trivial to extract secret key.

## Bugs & Credits

Please submit bugs/propositions via GitHub.

Original author: nshadov
