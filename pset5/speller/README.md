# Questions

## What is pneumonoultramicroscopicsilicovolcanoconiosis?

It is a lung disease caused by very fine ash and dust.

## According to its man page, what does `getrusage` do?

It gets the resource usage statistics for *who* and returns it to *rusage*.

## Per that same man page, how many members are in a variable of type `struct rusage`?

There are 16 members in `struct rusage`.

## Why do you think we pass `before` and `after` by reference (instead of by value) to `calculate`, even though we're not changing their contents?

When we pass by reference, we are making sure memory has been allocated to that structure by checking NULL condition.

## Explain as precisely as possible, in a paragraph or more, how `main` goes about reading words from a file. In other words, convince us that you indeed understand how that function's `for` loop works.

In the `for` loop given, we scan each and every character present in a file.

The first `if` construct is used to scan letters of a word as long as they're valid. The condition ensures only
characters or apostrophes in between characters are read (ex: could'nt) and stored in a word. If the length
were to exceed the maximum length, then that sequence of characters is read and discarded.

The `else if` construct reads and discards words with numbers in them.

The last `else` means a valid word is read and checked for spelling mistakes.

## Why do you think we used `fgetc` to read each word's characters one at a time rather than use `fscanf` with a format string like `"%s"` to read whole words at a time? Put another way, what problems might arise by relying on `fscanf` alone?

`fgetc` allows us to interact with every character and helps omit useless (sequence of character which are not
words) without using a checker function. This in case we have numbers in between, or if special characters are
present at the start of a word ("some_word"), etc.

## Why do you think we declared the parameters for `check` and `load` as `const` (which means "constant")?

This is done to probably ensure that we do not tamper with the name of dictionary file directory (since it is
`const`) and accidentaly manipulate memory which is not ours.
