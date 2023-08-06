hycl
========

[![Build Status](https://img.shields.io/travis/niitsuma/hycl/master.svg?style=flat-square)](https://travis-ci.org/niitsuma/hycl)

common-lisp-like functions and macros for hylang

Example
-------
```hy
(import   [hyclb.core [*]])
(require  [hyclb.core [*]])

(if/cl nil/cl True ) 
==> []


(dbind
 (a (b c) d) 
 (1 (2 3) 4)
 [a b c d])
 
==> [1 2 3 4]


(import   [hyclb.util [*]])
(require  [hyclb.util [*]])

(defun testfn2 (x y)
   (setq z 20)
   (if x (+ z y)))
   
(testfn2 [] 2)
==>  []

```


More examples can be found in the test
