%module(moduleimport="import $module") tmTable

%include <std_vector.i>
%include <std_string.i>
%include <std_map.i>

%{
#include "tmTable/tmTable.hh"
#include "tmTable/validator.hh"
%}


namespace std {
  %template(Row) map<string, string>;
  %template(Table) vector<map<string, string> >;
  %template(StringTableMap) map<string, vector<map<string, string> > >;
  %template(IntTableMap) map<int, vector<map<string, string> > >;
}

%include "tmTable/tmTable.hh"
%include "tmTable/validator.hh"
