NET-CONTEXTDIFF
===============

This package contains two main elements used to compare text-based
configuration files (or other files in simple text in a similar format) where
they are structured using indented blocks of directives/commands:

* a parser to read in configuration files and stored them in a dictionary --
  the parser utilises the hierarchical nature of the configuration to
  understand that the same command name might mean different things in
  different contexts

* a comparator that takes two configuration dictionaries (typically produced by
  the parser, above) - a source and a target configuration - and writes out
  a configuration file (or update command set) to transform the source
  configuration into the destination

Currently, only Cisco IOS configuration files can be parsed and compared, but
the parser and comparators (and the wrapper command line tool) are written such
that they should be extensible to new platforms (by creating new concrete
classes from the abstract toplevel classes).

At the present time, only a subset of configuration directives for Cisco IOS
are supported but more can be added, as required.

The scripts also support a system whereby rules can be included (rather like an
access control list) to specify which elements of the configuration are
included in the output.  This allows known differences to be ignored.
