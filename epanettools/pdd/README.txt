Now set_pdd will make all calls after that to be translated ENxxxx > ENxxxx_wrap!

To do: wrapper.h - all output variables have to be named and declared as output in pdd.i

Going back to check original (non-pdd) epanettools package to see if it properly does ENsetxxxx calls. 
(in this branch, they silently fail, as evidenced by ENsaveinpfile calls before and after!)