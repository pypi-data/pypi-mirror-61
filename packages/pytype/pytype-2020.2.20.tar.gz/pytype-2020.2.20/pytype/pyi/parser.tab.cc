// A Bison parser, made by GNU Bison 3.4.2.

// Skeleton implementation for Bison LALR(1) parsers in C++

// Copyright (C) 2002-2015, 2018-2019 Free Software Foundation, Inc.

// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.

// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.

// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.

// As a special exception, you may create a larger work that contains
// part or all of the Bison parser skeleton and distribute that work
// under terms of your choice, so long as that work isn't itself a
// parser generator using the skeleton or a modified version thereof
// as a parser skeleton.  Alternatively, if you modify or redistribute
// the parser skeleton itself, you may (at your option) remove this
// special exception, which will cause the skeleton and the resulting
// Bison output files to be licensed under the GNU General Public
// License without this special exception.

// This special exception was added by the Free Software Foundation in
// version 2.2 of Bison.

// Undocumented macros, especially those whose name start with YY_,
// are private implementation details.  Do not rely on them.


// Take the name prefix into account.
#define yylex   pytypelex



#include "parser.tab.hh"


// Unqualified %code blocks.
#line 34 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"

namespace {
PyObject* DOT_STRING = PyString_FromString(".");

/* Helper functions for building up lists. */
PyObject* StartList(PyObject* item);
PyObject* AppendList(PyObject* list, PyObject* item);
PyObject* ExtendList(PyObject* dst, PyObject* src);

}  // end namespace


// Check that a python value is not NULL.  This must be a macro because it
// calls YYERROR (which is a goto).
#define CHECK(x, loc) do { if (x == NULL) {\
    ctx->SetErrorLocation(loc); \
    YYERROR; \
  }} while(0)

// pytypelex is generated in lexer.lex.cc, but because it uses semantic_type and
// location, it must be declared here.
int pytypelex(pytype::parser::semantic_type* lvalp, pytype::location* llocp,
              void* scanner);


#line 73 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"


#ifndef YY_
# if defined YYENABLE_NLS && YYENABLE_NLS
#  if ENABLE_NLS
#   include <libintl.h> // FIXME: INFRINGES ON USER NAME SPACE.
#   define YY_(msgid) dgettext ("bison-runtime", msgid)
#  endif
# endif
# ifndef YY_
#  define YY_(msgid) msgid
# endif
#endif

// Whether we are compiled with exception support.
#ifndef YY_EXCEPTIONS
# if defined __GNUC__ && !defined __EXCEPTIONS
#  define YY_EXCEPTIONS 0
# else
#  define YY_EXCEPTIONS 1
# endif
#endif

#define YYRHSLOC(Rhs, K) ((Rhs)[K].location)
/* YYLLOC_DEFAULT -- Set CURRENT to span from RHS[1] to RHS[N].
   If N is 0, then set CURRENT to the empty location which ends
   the previous symbol: RHS[0] (always defined).  */

# ifndef YYLLOC_DEFAULT
#  define YYLLOC_DEFAULT(Current, Rhs, N)                               \
    do                                                                  \
      if (N)                                                            \
        {                                                               \
          (Current).begin  = YYRHSLOC (Rhs, 1).begin;                   \
          (Current).end    = YYRHSLOC (Rhs, N).end;                     \
        }                                                               \
      else                                                              \
        {                                                               \
          (Current).begin = (Current).end = YYRHSLOC (Rhs, 0).end;      \
        }                                                               \
    while (false)
# endif


// Enable debugging if requested.
#if PYTYPEDEBUG

// A pseudo ostream that takes yydebug_ into account.
# define YYCDEBUG if (yydebug_) (*yycdebug_)

# define YY_SYMBOL_PRINT(Title, Symbol)         \
  do {                                          \
    if (yydebug_)                               \
    {                                           \
      *yycdebug_ << Title << ' ';               \
      yy_print_ (*yycdebug_, Symbol);           \
      *yycdebug_ << '\n';                       \
    }                                           \
  } while (false)

# define YY_REDUCE_PRINT(Rule)          \
  do {                                  \
    if (yydebug_)                       \
      yy_reduce_print_ (Rule);          \
  } while (false)

# define YY_STACK_PRINT()               \
  do {                                  \
    if (yydebug_)                       \
      yystack_print_ ();                \
  } while (false)

#else // !PYTYPEDEBUG

# define YYCDEBUG if (false) std::cerr
# define YY_SYMBOL_PRINT(Title, Symbol)  YYUSE (Symbol)
# define YY_REDUCE_PRINT(Rule)           static_cast<void> (0)
# define YY_STACK_PRINT()                static_cast<void> (0)

#endif // !PYTYPEDEBUG

#define yyerrok         (yyerrstatus_ = 0)
#define yyclearin       (yyla.clear ())

#define YYACCEPT        goto yyacceptlab
#define YYABORT         goto yyabortlab
#define YYERROR         goto yyerrorlab
#define YYRECOVERING()  (!!yyerrstatus_)

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
namespace pytype {
#line 165 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"


  /* Return YYSTR after stripping away unnecessary quotes and
     backslashes, so that it's suitable for yyerror.  The heuristic is
     that double-quoting is unnecessary unless the string contains an
     apostrophe, a comma, or backslash (other than backslash-backslash).
     YYSTR is taken from yytname.  */
  std::string
  parser::yytnamerr_ (const char *yystr)
  {
    if (*yystr == '"')
      {
        std::string yyr;
        char const *yyp = yystr;

        for (;;)
          switch (*++yyp)
            {
            case '\'':
            case ',':
              goto do_not_strip_quotes;

            case '\\':
              if (*++yyp != '\\')
                goto do_not_strip_quotes;
              else
                goto append;

            append:
            default:
              yyr += *yyp;
              break;

            case '"':
              return yyr;
            }
      do_not_strip_quotes: ;
      }

    return yystr;
  }


  /// Build a parser object.
  parser::parser (void* scanner_yyarg, pytype::Context* ctx_yyarg)
    :
#if PYTYPEDEBUG
      yydebug_ (false),
      yycdebug_ (&std::cerr),
#endif
      scanner (scanner_yyarg),
      ctx (ctx_yyarg)
  {}

  parser::~parser ()
  {}

  parser::syntax_error::~syntax_error () YY_NOEXCEPT YY_NOTHROW
  {}

  /*---------------.
  | Symbol types.  |
  `---------------*/

  // basic_symbol.
#if 201103L <= YY_CPLUSPLUS
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (basic_symbol&& that)
    : Base (std::move (that))
    , value (std::move (that.value))
    , location (std::move (that.location))
  {}
#endif

  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (const basic_symbol& that)
    : Base (that)
    , value (that.value)
    , location (that.location)
  {}


  /// Constructor for valueless symbols.
  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_MOVE_REF (location_type) l)
    : Base (t)
    , value ()
    , location (l)
  {}

  template <typename Base>
  parser::basic_symbol<Base>::basic_symbol (typename Base::kind_type t, YY_RVREF (semantic_type) v, YY_RVREF (location_type) l)
    : Base (t)
    , value (YY_MOVE (v))
    , location (YY_MOVE (l))
  {}

  template <typename Base>
  bool
  parser::basic_symbol<Base>::empty () const YY_NOEXCEPT
  {
    return Base::type_get () == empty_symbol;
  }

  template <typename Base>
  void
  parser::basic_symbol<Base>::move (basic_symbol& s)
  {
    super_type::move (s);
    value = YY_MOVE (s.value);
    location = YY_MOVE (s.location);
  }

  // by_type.
  parser::by_type::by_type ()
    : type (empty_symbol)
  {}

#if 201103L <= YY_CPLUSPLUS
  parser::by_type::by_type (by_type&& that)
    : type (that.type)
  {
    that.clear ();
  }
#endif

  parser::by_type::by_type (const by_type& that)
    : type (that.type)
  {}

  parser::by_type::by_type (token_type t)
    : type (yytranslate_ (t))
  {}

  void
  parser::by_type::clear ()
  {
    type = empty_symbol;
  }

  void
  parser::by_type::move (by_type& that)
  {
    type = that.type;
    that.clear ();
  }

  int
  parser::by_type::type_get () const YY_NOEXCEPT
  {
    return type;
  }


  // by_state.
  parser::by_state::by_state () YY_NOEXCEPT
    : state (empty_state)
  {}

  parser::by_state::by_state (const by_state& that) YY_NOEXCEPT
    : state (that.state)
  {}

  void
  parser::by_state::clear () YY_NOEXCEPT
  {
    state = empty_state;
  }

  void
  parser::by_state::move (by_state& that)
  {
    state = that.state;
    that.clear ();
  }

  parser::by_state::by_state (state_type s) YY_NOEXCEPT
    : state (s)
  {}

  parser::symbol_number_type
  parser::by_state::type_get () const YY_NOEXCEPT
  {
    if (state == empty_state)
      return empty_symbol;
    else
      return yystos_[state];
  }

  parser::stack_symbol_type::stack_symbol_type ()
  {}

  parser::stack_symbol_type::stack_symbol_type (YY_RVREF (stack_symbol_type) that)
    : super_type (YY_MOVE (that.state), YY_MOVE (that.value), YY_MOVE (that.location))
  {
#if 201103L <= YY_CPLUSPLUS
    // that is emptied.
    that.state = empty_state;
#endif
  }

  parser::stack_symbol_type::stack_symbol_type (state_type s, YY_MOVE_REF (symbol_type) that)
    : super_type (s, YY_MOVE (that.value), YY_MOVE (that.location))
  {
    // that is emptied.
    that.type = empty_symbol;
  }

#if YY_CPLUSPLUS < 201103L
  parser::stack_symbol_type&
  parser::stack_symbol_type::operator= (stack_symbol_type& that)
  {
    state = that.state;
    value = that.value;
    location = that.location;
    // that is emptied.
    that.state = empty_state;
    return *this;
  }
#endif

  template <typename Base>
  void
  parser::yy_destroy_ (const char* yymsg, basic_symbol<Base>& yysym) const
  {
    if (yymsg)
      YY_SYMBOL_PRINT (yymsg, yysym);

    // User destructor.
    switch (yysym.type_get ())
    {
      case 3: // NAME
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 400 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 4: // NUMBER
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 406 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 5: // STRING
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 412 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 6: // LEXERROR
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 418 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 48: // start
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 424 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 49: // unit
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 430 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 50: // alldefs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 436 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 52: // classdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 442 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 53: // class_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 448 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 54: // parents
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 454 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 55: // parent_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 460 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 56: // parent
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 466 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 57: // maybe_class_funcs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 472 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 58: // class_funcs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 478 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 59: // funcdefs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 484 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 60: // if_stmt
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 490 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 61: // if_and_elifs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 496 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 62: // class_if_stmt
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 502 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 63: // class_if_and_elifs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 508 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 64: // if_cond
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 514 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 65: // elif_cond
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 520 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 66: // else_cond
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 526 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 67: // condition
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 532 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 68: // version_tuple
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 538 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 69: // condition_op
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.str)); }
#line 544 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 70: // constantdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 550 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 71: // importdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 556 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 72: // import_items
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 562 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 73: // import_item
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 568 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 74: // import_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 574 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 75: // from_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 580 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 76: // from_items
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 586 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 77: // from_item
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 592 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 78: // alias_or_constant
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 598 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 79: // maybe_string_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 604 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 80: // string_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 610 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 81: // typevardef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 616 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 82: // typevar_args
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 622 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 83: // typevar_kwargs
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 628 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 84: // typevar_kwarg
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 634 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 85: // funcdef
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 640 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 86: // funcname
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 646 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 87: // decorators
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 652 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 88: // decorator
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 658 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 89: // maybe_async
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 664 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 90: // params
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 670 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 91: // param_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 676 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 92: // param
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 682 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 93: // param_type
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 688 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 94: // param_default
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 694 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 95: // param_star_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 700 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 96: // return
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 706 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 98: // maybe_body
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 712 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 100: // body
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 718 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 101: // body_stmt
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 724 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 102: // type_parameters
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 730 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 103: // type_parameter
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 736 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 104: // maybe_type_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 742 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 105: // type_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 748 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 106: // type
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 754 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 107: // named_tuple_fields
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 760 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 108: // named_tuple_field_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 766 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 109: // named_tuple_field
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 772 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 111: // coll_named_tuple_fields
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 778 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 112: // coll_named_tuple_field_list
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 784 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 113: // coll_named_tuple_field
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 790 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 114: // type_tuple_elements
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 796 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 115: // type_tuple_literal
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 802 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 116: // dotted_name
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 808 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 117: // getitem_key
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 814 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      case 118: // maybe_number
#line 101 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
        { Py_CLEAR((yysym.value.obj)); }
#line 820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
        break;

      default:
        break;
    }
  }

#if PYTYPEDEBUG
  template <typename Base>
  void
  parser::yy_print_ (std::ostream& yyo,
                                     const basic_symbol<Base>& yysym) const
  {
    std::ostream& yyoutput = yyo;
    YYUSE (yyoutput);
    symbol_number_type yytype = yysym.type_get ();
#if defined __GNUC__ && ! defined __clang__ && ! defined __ICC && __GNUC__ * 100 + __GNUC_MINOR__ <= 408
    // Avoid a (spurious) G++ 4.8 warning about "array subscript is
    // below array bounds".
    if (yysym.empty ())
      std::abort ();
#endif
    yyo << (yytype < yyntokens_ ? "token" : "nterm")
        << ' ' << yytname_[yytype] << " ("
        << yysym.location << ": ";
    YYUSE (yytype);
    yyo << ')';
  }
#endif

  void
  parser::yypush_ (const char* m, YY_MOVE_REF (stack_symbol_type) sym)
  {
    if (m)
      YY_SYMBOL_PRINT (m, sym);
    yystack_.push (YY_MOVE (sym));
  }

  void
  parser::yypush_ (const char* m, state_type s, YY_MOVE_REF (symbol_type) sym)
  {
#if 201103L <= YY_CPLUSPLUS
    yypush_ (m, stack_symbol_type (s, std::move (sym)));
#else
    stack_symbol_type ss (s, sym);
    yypush_ (m, ss);
#endif
  }

  void
  parser::yypop_ (int n)
  {
    yystack_.pop (n);
  }

#if PYTYPEDEBUG
  std::ostream&
  parser::debug_stream () const
  {
    return *yycdebug_;
  }

  void
  parser::set_debug_stream (std::ostream& o)
  {
    yycdebug_ = &o;
  }


  parser::debug_level_type
  parser::debug_level () const
  {
    return yydebug_;
  }

  void
  parser::set_debug_level (debug_level_type l)
  {
    yydebug_ = l;
  }
#endif // PYTYPEDEBUG

  parser::state_type
  parser::yy_lr_goto_state_ (state_type yystate, int yysym)
  {
    int yyr = yypgoto_[yysym - yyntokens_] + yystate;
    if (0 <= yyr && yyr <= yylast_ && yycheck_[yyr] == yystate)
      return yytable_[yyr];
    else
      return yydefgoto_[yysym - yyntokens_];
  }

  bool
  parser::yy_pact_value_is_default_ (int yyvalue)
  {
    return yyvalue == yypact_ninf_;
  }

  bool
  parser::yy_table_value_is_error_ (int yyvalue)
  {
    return yyvalue == yytable_ninf_;
  }

  int
  parser::operator() ()
  {
    return parse ();
  }

  int
  parser::parse ()
  {
    // State.
    int yyn;
    /// Length of the RHS of the rule being reduced.
    int yylen = 0;

    // Error handling.
    int yynerrs_ = 0;
    int yyerrstatus_ = 0;

    /// The lookahead symbol.
    symbol_type yyla;

    /// The locations where the error started and ended.
    stack_symbol_type yyerror_range[3];

    /// The return value of parse ().
    int yyresult;

#if YY_EXCEPTIONS
    try
#endif // YY_EXCEPTIONS
      {
    YYCDEBUG << "Starting parse\n";


    /* Initialize the stack.  The initial state will be set in
       yynewstate, since the latter expects the semantical and the
       location values to have been already stored, initialize these
       stacks with a primary value.  */
    yystack_.clear ();
    yypush_ (YY_NULLPTR, 0, YY_MOVE (yyla));

  /*-----------------------------------------------.
  | yynewstate -- push a new symbol on the stack.  |
  `-----------------------------------------------*/
  yynewstate:
    YYCDEBUG << "Entering state " << yystack_[0].state << '\n';

    // Accept?
    if (yystack_[0].state == yyfinal_)
      YYACCEPT;

    goto yybackup;


  /*-----------.
  | yybackup.  |
  `-----------*/
  yybackup:
    // Try to take a decision without lookahead.
    yyn = yypact_[yystack_[0].state];
    if (yy_pact_value_is_default_ (yyn))
      goto yydefault;

    // Read a lookahead token.
    if (yyla.empty ())
      {
        YYCDEBUG << "Reading a token: ";
#if YY_EXCEPTIONS
        try
#endif // YY_EXCEPTIONS
          {
            yyla.type = yytranslate_ (yylex (&yyla.value, &yyla.location, scanner));
          }
#if YY_EXCEPTIONS
        catch (const syntax_error& yyexc)
          {
            YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
            error (yyexc);
            goto yyerrlab1;
          }
#endif // YY_EXCEPTIONS
      }
    YY_SYMBOL_PRINT ("Next token is", yyla);

    /* If the proper action on seeing token YYLA.TYPE is to reduce or
       to detect an error, take that action.  */
    yyn += yyla.type_get ();
    if (yyn < 0 || yylast_ < yyn || yycheck_[yyn] != yyla.type_get ())
      goto yydefault;

    // Reduce or error.
    yyn = yytable_[yyn];
    if (yyn <= 0)
      {
        if (yy_table_value_is_error_ (yyn))
          goto yyerrlab;
        yyn = -yyn;
        goto yyreduce;
      }

    // Count tokens shifted since error; after three, turn off error status.
    if (yyerrstatus_)
      --yyerrstatus_;

    // Shift the lookahead token.
    yypush_ ("Shifting", yyn, YY_MOVE (yyla));
    goto yynewstate;


  /*-----------------------------------------------------------.
  | yydefault -- do the default action for the current state.  |
  `-----------------------------------------------------------*/
  yydefault:
    yyn = yydefact_[yystack_[0].state];
    if (yyn == 0)
      goto yyerrlab;
    goto yyreduce;


  /*-----------------------------.
  | yyreduce -- do a reduction.  |
  `-----------------------------*/
  yyreduce:
    yylen = yyr2_[yyn];
    {
      stack_symbol_type yylhs;
      yylhs.state = yy_lr_goto_state_ (yystack_[yylen].state, yyr1_[yyn]);
      /* If YYLEN is nonzero, implement the default value of the
         action: '$$ = $1'.  Otherwise, use the top of the stack.

         Otherwise, the following line sets YYLHS.VALUE to garbage.
         This behavior is undocumented and Bison users should not rely
         upon it.  */
      if (yylen)
        yylhs.value = yystack_[yylen - 1].value;
      else
        yylhs.value = yystack_[0].value;

      // Default location.
      {
        stack_type::slice range (yystack_, yylen);
        YYLLOC_DEFAULT (yylhs.location, range, yylen);
        yyerror_range[1].location = yylhs.location;
      }

      // Perform the reduction.
      YY_REDUCE_PRINT (yyn);
#if YY_EXCEPTIONS
      try
#endif // YY_EXCEPTIONS
        {
          switch (yyn)
            {
  case 2:
#line 134 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1081 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 3:
#line 135 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { ctx->SetAndDelResult((yystack_[1].value.obj)); (yylhs.value.obj) = NULL; }
#line 1087 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 4:
#line 139 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1093 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 5:
#line 143 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1099 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 6:
#line 144 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1105 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 7:
#line 145 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1111 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 8:
#line 146 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = (yystack_[1].value.obj);
      PyObject* tmp = ctx->Call(kAddAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
    }
#line 1122 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 9:
#line 152 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1128 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 10:
#line 153 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); Py_DECREF((yystack_[0].value.obj)); }
#line 1134 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 11:
#line 154 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1144 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 12:
#line 159 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1150 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 15:
#line 172 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewClass, "(NNNN)", (yystack_[6].value.obj), (yystack_[4].value.obj), (yystack_[3].value.obj), (yystack_[0].value.obj));
      // Fix location tracking. See funcdef.
      yylhs.location.begin = yystack_[4].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1161 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 16:
#line 181 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      // Do not borrow the $1 reference since it is also returned later
      // in $$.  Use O instead of N in the format string.
      PyObject* tmp = ctx->Call(kRegisterClassName, "(O)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      Py_DECREF(tmp);
      (yylhs.value.obj) = (yystack_[0].value.obj);
    }
#line 1174 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 17:
#line 192 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1180 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 18:
#line 193 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1186 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 19:
#line 194 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1192 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 20:
#line 198 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1198 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 21:
#line 199 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1204 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 22:
#line 203 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1210 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 23:
#line 204 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1216 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 24:
#line 205 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyString_FromString("NamedTuple"); }
#line 1222 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 25:
#line 209 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1228 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 26:
#line 210 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1234 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 27:
#line 211 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1240 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 28:
#line 215 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1246 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 29:
#line 216 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1252 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 30:
#line 220 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1258 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 31:
#line 221 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      PyObject* tmp = ctx->Call(kNewAliasOrConstant, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yylhs.location);
      (yylhs.value.obj) = AppendList((yystack_[1].value.obj), tmp);
    }
#line 1268 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 32:
#line 226 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1274 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 33:
#line 227 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      PyObject* tmp = ctx->Call(kIfEnd, "(N)", (yystack_[0].value.obj));
      CHECK(tmp, yystack_[0].location);
      (yylhs.value.obj) = ExtendList((yystack_[1].value.obj), tmp);
    }
#line 1284 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 34:
#line 232 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1290 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 35:
#line 233 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1296 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 36:
#line 238 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1304 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 37:
#line 241 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1310 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 38:
#line 246 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1318 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 39:
#line 250 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1326 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 40:
#line 269 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1334 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 41:
#line 272 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1340 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 42:
#line 277 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = Py_BuildValue("[(NN)]", (yystack_[4].value.obj), (yystack_[1].value.obj));
    }
#line 1348 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 43:
#line 281 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = AppendList((yystack_[5].value.obj), Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)));
    }
#line 1356 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 44:
#line 293 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Call(kIfBegin, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1362 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 45:
#line 297 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Call(kIfElif, "(N)", (yystack_[0].value.obj)); CHECK((yylhs.value.obj), yylhs.location); }
#line 1368 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 46:
#line 301 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Call(kIfElse, "()"); CHECK((yylhs.value.obj), yylhs.location); }
#line 1374 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 47:
#line 305 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1382 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 48:
#line 308 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = Py_BuildValue("((NO)sN)", (yystack_[2].value.obj), Py_None, (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1390 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 49:
#line 311 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1398 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 50:
#line 314 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = Py_BuildValue("((NN)sN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.str), (yystack_[0].value.obj));
    }
#line 1406 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 51:
#line 317 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "and", (yystack_[0].value.obj)); }
#line 1412 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 52:
#line 318 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NsN)", (yystack_[2].value.obj), "or", (yystack_[0].value.obj)); }
#line 1418 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 53:
#line 319 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1424 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 54:
#line 324 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(N)", (yystack_[2].value.obj)); }
#line 1430 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 55:
#line 325 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj)); }
#line 1436 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 56:
#line 326 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj));
    }
#line 1444 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 57:
#line 332 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.str) = "<"; }
#line 1450 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 58:
#line 333 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.str) = ">"; }
#line 1456 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 59:
#line 334 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.str) = "<="; }
#line 1462 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 60:
#line 335 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.str) = ">="; }
#line 1468 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 61:
#line 336 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.str) = "=="; }
#line 1474 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 62:
#line 337 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.str) = "!="; }
#line 1480 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 63:
#line 341 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1489 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 64:
#line 345 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1498 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 65:
#line 349 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1507 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 66:
#line 353 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[2].value.obj), ctx->Value(kAnything));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1516 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 67:
#line 357 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1525 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 68:
#line 361 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1534 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 69:
#line 365 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewConstant, "(NN)", (yystack_[5].value.obj), (yystack_[3].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1543 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 70:
#line 372 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(ON)", Py_None, (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1552 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 71:
#line 376 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kAddImport, "(NN)", (yystack_[3].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1561 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 72:
#line 380 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      // Special-case "from . import" and pass in a __PACKAGE__ token that
      // the Python parser code will rewrite to the current package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PACKAGE__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1572 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 73:
#line 386 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      // Special-case "from .. import" and pass in a __PARENT__ token that
      // the Python parser code will rewrite to the parent package name.
      (yylhs.value.obj) = ctx->Call(kAddImport, "(sN)", "__PARENT__", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1583 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 74:
#line 395 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1589 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 75:
#line 396 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1595 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 76:
#line 400 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1601 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 77:
#line 401 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1607 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 78:
#line 406 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1613 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 79:
#line 407 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = PyString_FromFormat(".%s", PyString_AsString((yystack_[0].value.obj)));
      Py_DECREF((yystack_[0].value.obj));
    }
#line 1622 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 80:
#line 414 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1628 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 81:
#line 415 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1634 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 82:
#line 416 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 1640 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 83:
#line 420 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1646 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 84:
#line 421 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1652 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 85:
#line 425 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1658 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 86:
#line 426 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = PyString_FromString("NamedTuple");
    }
#line 1666 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 87:
#line 429 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = PyString_FromString("namedtuple");
    }
#line 1674 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 88:
#line 432 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = PyString_FromString("TypeVar");
    }
#line 1682 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 89:
#line 435 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = PyString_FromString("*");
    }
#line 1690 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 90:
#line 438 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1696 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 91:
#line 442 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1702 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 92:
#line 443 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[1].value.obj)); }
#line 1708 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 93:
#line 447 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1714 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 94:
#line 448 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1720 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 95:
#line 452 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1726 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 96:
#line 453 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1732 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 97:
#line 457 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kAddTypeVar, "(NNN)", (yystack_[6].value.obj), (yystack_[2].value.obj), (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1741 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 98:
#line 464 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(OO)", Py_None, Py_None); }
#line 1747 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 99:
#line 465 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NO)", (yystack_[0].value.obj), Py_None); }
#line 1753 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 100:
#line 466 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(ON)", Py_None, (yystack_[0].value.obj)); }
#line 1759 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 101:
#line 467 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1765 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 102:
#line 471 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1771 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 103:
#line 472 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1777 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 104:
#line 476 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1783 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 105:
#line 478 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 1789 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 106:
#line 482 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewFunction, "(NONNNN)", (yystack_[8].value.obj), (yystack_[7].value.obj), (yystack_[5].value.obj), (yystack_[3].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj));
      // Decorators is nullable and messes up the location tracking by
      // using the previous symbol as the start location for this production,
      // which is very misleading.  It is better to ignore decorators and
      // pretend the production started with DEF.  Even when decorators are
      // present the error line will be close enough to be helpful.
      //
      // TODO(dbaum): Consider making this smarter and only ignoring decorators
      // when they are empty.  Making decorators non-nullable and having two
      // productions for funcdef would be a reasonable solution.
      yylhs.location.begin = yystack_[6].location.begin;
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 1808 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 107:
#line 499 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1814 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 108:
#line 500 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyString_FromString("namedtuple"); }
#line 1820 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 109:
#line 504 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1826 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 110:
#line 505 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1832 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 111:
#line 509 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1838 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 112:
#line 513 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_True; }
#line 1844 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 113:
#line 514 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_False; }
#line 1850 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 114:
#line 518 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1856 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 115:
#line 519 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1862 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 116:
#line 531 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[3].value.obj), (yystack_[0].value.obj)); }
#line 1868 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 117:
#line 532 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1874 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 118:
#line 536 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NNN)", (yystack_[2].value.obj), (yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1880 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 119:
#line 537 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(sOO)", "*", Py_None, Py_None); }
#line 1886 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 120:
#line 538 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NNO)", (yystack_[1].value.obj), (yystack_[0].value.obj), Py_None); }
#line 1892 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 121:
#line 539 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1898 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 122:
#line 543 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1904 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 123:
#line 544 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1910 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 124:
#line 548 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1916 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 125:
#line 549 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1922 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 126:
#line 550 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 1928 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 127:
#line 551 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { Py_INCREF(Py_None); (yylhs.value.obj) = Py_None; }
#line 1934 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 128:
#line 555 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyString_FromFormat("*%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1940 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 129:
#line 556 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyString_FromFormat("**%s", PyString_AsString((yystack_[0].value.obj))); }
#line 1946 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 130:
#line 560 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 1952 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 131:
#line 561 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 1958 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 132:
#line 565 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { Py_DecRef((yystack_[0].value.obj)); }
#line 1964 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 133:
#line 569 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1970 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 134:
#line 570 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 1976 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 135:
#line 571 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 1982 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 143:
#line 585 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[1].value.obj), (yystack_[0].value.obj)); }
#line 1988 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 144:
#line 586 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 1994 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 145:
#line 590 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2000 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 146:
#line 591 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2006 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 147:
#line 592 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2012 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 148:
#line 596 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2018 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 149:
#line 597 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2024 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 150:
#line 601 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2030 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 151:
#line 602 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Value(kEllipsis); }
#line 2036 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 152:
#line 604 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2042 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 153:
#line 605 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2048 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 154:
#line 607 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(sN)", "tuple", (yystack_[1].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2057 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 155:
#line 614 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2063 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 156:
#line 615 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 2069 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 157:
#line 619 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2075 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 158:
#line 620 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2081 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 159:
#line 624 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(N)", (yystack_[0].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2090 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 160:
#line 628 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), PyList_New(0));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2099 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 161:
#line 632 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewType, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2108 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 162:
#line 636 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2117 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 163:
#line 640 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = ctx->Call(kNewNamedTuple, "(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj));
      CHECK((yylhs.value.obj), yylhs.location);
    }
#line 2126 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 164:
#line 644 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[1].value.obj); }
#line 2132 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 165:
#line 645 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Call(kNewIntersectionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2138 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 166:
#line 646 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Call(kNewUnionType, "([NN])", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2144 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 167:
#line 647 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Value(kAnything); }
#line 2150 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 168:
#line 648 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = ctx->Value(kNothing); }
#line 2156 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 169:
#line 652 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2162 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 170:
#line 653 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 2168 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 171:
#line 657 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2174 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 172:
#line 658 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2180 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 173:
#line 662 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[4].value.obj), (yystack_[2].value.obj)); }
#line 2186 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 176:
#line 671 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[2].value.obj); }
#line 2192 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 177:
#line 672 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = PyList_New(0); }
#line 2198 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 178:
#line 676 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj));
    }
#line 2206 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 179:
#line 679 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = StartList((yystack_[0].value.obj)); }
#line 2212 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 180:
#line 683 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[0].value.obj), ctx->Value(kAnything)); }
#line 2218 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 181:
#line 690 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = AppendList((yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2224 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 182:
#line 691 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = Py_BuildValue("(NN)", (yystack_[2].value.obj), (yystack_[0].value.obj)); }
#line 2230 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 183:
#line 700 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2239 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 184:
#line 705 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      Py_DECREF((yystack_[2].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2248 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 185:
#line 711 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      Py_DECREF((yystack_[1].value.obj));
      (yylhs.value.obj) = ctx->Value(kTuple);
    }
#line 2257 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 186:
#line 718 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2263 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 187:
#line 719 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
#if PY_MAJOR_VERSION >= 3
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), DOT_STRING);
      (yystack_[2].value.obj) = PyUnicode_Concat((yystack_[2].value.obj), (yystack_[0].value.obj));
      Py_DECREF((yystack_[0].value.obj));
#else
      PyString_Concat(&(yystack_[2].value.obj), DOT_STRING);
      PyString_ConcatAndDel(&(yystack_[2].value.obj), (yystack_[0].value.obj));
#endif
      (yylhs.value.obj) = (yystack_[2].value.obj);
    }
#line 2279 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 188:
#line 733 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2285 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 189:
#line 734 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      PyObject* slice = PySlice_New((yystack_[2].value.obj), (yystack_[0].value.obj), NULL);
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2295 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 190:
#line 739 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    {
      PyObject* slice = PySlice_New((yystack_[4].value.obj), (yystack_[2].value.obj), (yystack_[0].value.obj));
      CHECK(slice, yylhs.location);
      (yylhs.value.obj) = slice;
    }
#line 2305 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 191:
#line 747 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = (yystack_[0].value.obj); }
#line 2311 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;

  case 192:
#line 748 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
    { (yylhs.value.obj) = NULL; }
#line 2317 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"
    break;


#line 2321 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

            default:
              break;
            }
        }
#if YY_EXCEPTIONS
      catch (const syntax_error& yyexc)
        {
          YYCDEBUG << "Caught exception: " << yyexc.what() << '\n';
          error (yyexc);
          YYERROR;
        }
#endif // YY_EXCEPTIONS
      YY_SYMBOL_PRINT ("-> $$ =", yylhs);
      yypop_ (yylen);
      yylen = 0;
      YY_STACK_PRINT ();

      // Shift the result of the reduction.
      yypush_ (YY_NULLPTR, YY_MOVE (yylhs));
    }
    goto yynewstate;


  /*--------------------------------------.
  | yyerrlab -- here on detecting error.  |
  `--------------------------------------*/
  yyerrlab:
    // If not already recovering from an error, report this error.
    if (!yyerrstatus_)
      {
        ++yynerrs_;
        error (yyla.location, yysyntax_error_ (yystack_[0].state, yyla));
      }


    yyerror_range[1].location = yyla.location;
    if (yyerrstatus_ == 3)
      {
        /* If just tried and failed to reuse lookahead token after an
           error, discard it.  */

        // Return failure if at end of input.
        if (yyla.type_get () == yyeof_)
          YYABORT;
        else if (!yyla.empty ())
          {
            yy_destroy_ ("Error: discarding", yyla);
            yyla.clear ();
          }
      }

    // Else will try to reuse lookahead token after shifting the error token.
    goto yyerrlab1;


  /*---------------------------------------------------.
  | yyerrorlab -- error raised explicitly by YYERROR.  |
  `---------------------------------------------------*/
  yyerrorlab:
    /* Pacify compilers when the user code never invokes YYERROR and
       the label yyerrorlab therefore never appears in user code.  */
    if (false)
      YYERROR;

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYERROR.  */
    yypop_ (yylen);
    yylen = 0;
    goto yyerrlab1;


  /*-------------------------------------------------------------.
  | yyerrlab1 -- common code for both syntax error and YYERROR.  |
  `-------------------------------------------------------------*/
  yyerrlab1:
    yyerrstatus_ = 3;   // Each real token shifted decrements this.
    {
      stack_symbol_type error_token;
      for (;;)
        {
          yyn = yypact_[yystack_[0].state];
          if (!yy_pact_value_is_default_ (yyn))
            {
              yyn += yyterror_;
              if (0 <= yyn && yyn <= yylast_ && yycheck_[yyn] == yyterror_)
                {
                  yyn = yytable_[yyn];
                  if (0 < yyn)
                    break;
                }
            }

          // Pop the current state because it cannot handle the error token.
          if (yystack_.size () == 1)
            YYABORT;

          yyerror_range[1].location = yystack_[0].location;
          yy_destroy_ ("Error: popping", yystack_[0]);
          yypop_ ();
          YY_STACK_PRINT ();
        }

      yyerror_range[2].location = yyla.location;
      YYLLOC_DEFAULT (error_token.location, yyerror_range, 2);

      // Shift the error token.
      error_token.state = yyn;
      yypush_ ("Shifting", YY_MOVE (error_token));
    }
    goto yynewstate;


  /*-------------------------------------.
  | yyacceptlab -- YYACCEPT comes here.  |
  `-------------------------------------*/
  yyacceptlab:
    yyresult = 0;
    goto yyreturn;


  /*-----------------------------------.
  | yyabortlab -- YYABORT comes here.  |
  `-----------------------------------*/
  yyabortlab:
    yyresult = 1;
    goto yyreturn;


  /*-----------------------------------------------------.
  | yyreturn -- parsing is finished, return the result.  |
  `-----------------------------------------------------*/
  yyreturn:
    if (!yyla.empty ())
      yy_destroy_ ("Cleanup: discarding lookahead", yyla);

    /* Do not reclaim the symbols of the rule whose action triggered
       this YYABORT or YYACCEPT.  */
    yypop_ (yylen);
    while (1 < yystack_.size ())
      {
        yy_destroy_ ("Cleanup: popping", yystack_[0]);
        yypop_ ();
      }

    return yyresult;
  }
#if YY_EXCEPTIONS
    catch (...)
      {
        YYCDEBUG << "Exception caught: cleaning lookahead and stack\n";
        // Do not try to display the values of the reclaimed symbols,
        // as their printers might throw an exception.
        if (!yyla.empty ())
          yy_destroy_ (YY_NULLPTR, yyla);

        while (1 < yystack_.size ())
          {
            yy_destroy_ (YY_NULLPTR, yystack_[0]);
            yypop_ ();
          }
        throw;
      }
#endif // YY_EXCEPTIONS
  }

  void
  parser::error (const syntax_error& yyexc)
  {
    error (yyexc.location, yyexc.what ());
  }

  // Generate an error message.
  std::string
  parser::yysyntax_error_ (state_type yystate, const symbol_type& yyla) const
  {
    // Number of reported tokens (one for the "unexpected", one per
    // "expected").
    size_t yycount = 0;
    // Its maximum.
    enum { YYERROR_VERBOSE_ARGS_MAXIMUM = 5 };
    // Arguments of yyformat.
    char const *yyarg[YYERROR_VERBOSE_ARGS_MAXIMUM];

    /* There are many possibilities here to consider:
       - If this state is a consistent state with a default action, then
         the only way this function was invoked is if the default action
         is an error action.  In that case, don't check for expected
         tokens because there are none.
       - The only way there can be no lookahead present (in yyla) is
         if this state is a consistent state with a default action.
         Thus, detecting the absence of a lookahead is sufficient to
         determine that there is no unexpected or expected token to
         report.  In that case, just report a simple "syntax error".
       - Don't assume there isn't a lookahead just because this state is
         a consistent state with a default action.  There might have
         been a previous inconsistent state, consistent state with a
         non-default action, or user semantic action that manipulated
         yyla.  (However, yyla is currently not documented for users.)
       - Of course, the expected token list depends on states to have
         correct lookahead information, and it depends on the parser not
         to perform extra reductions after fetching a lookahead from the
         scanner and before detecting a syntax error.  Thus, state
         merging (from LALR or IELR) and default reductions corrupt the
         expected token list.  However, the list is correct for
         canonical LR with one exception: it will still contain any
         token that will not be accepted due to an error action in a
         later state.
    */
    if (!yyla.empty ())
      {
        int yytoken = yyla.type_get ();
        yyarg[yycount++] = yytname_[yytoken];
        int yyn = yypact_[yystate];
        if (!yy_pact_value_is_default_ (yyn))
          {
            /* Start YYX at -YYN if negative to avoid negative indexes in
               YYCHECK.  In other words, skip the first -YYN actions for
               this state because they are default actions.  */
            int yyxbegin = yyn < 0 ? -yyn : 0;
            // Stay within bounds of both yycheck and yytname.
            int yychecklim = yylast_ - yyn + 1;
            int yyxend = yychecklim < yyntokens_ ? yychecklim : yyntokens_;
            for (int yyx = yyxbegin; yyx < yyxend; ++yyx)
              if (yycheck_[yyx + yyn] == yyx && yyx != yyterror_
                  && !yy_table_value_is_error_ (yytable_[yyx + yyn]))
                {
                  if (yycount == YYERROR_VERBOSE_ARGS_MAXIMUM)
                    {
                      yycount = 1;
                      break;
                    }
                  else
                    yyarg[yycount++] = yytname_[yyx];
                }
          }
      }

    char const* yyformat = YY_NULLPTR;
    switch (yycount)
      {
#define YYCASE_(N, S)                         \
        case N:                               \
          yyformat = S;                       \
        break
      default: // Avoid compiler warnings.
        YYCASE_ (0, YY_("syntax error"));
        YYCASE_ (1, YY_("syntax error, unexpected %s"));
        YYCASE_ (2, YY_("syntax error, unexpected %s, expecting %s"));
        YYCASE_ (3, YY_("syntax error, unexpected %s, expecting %s or %s"));
        YYCASE_ (4, YY_("syntax error, unexpected %s, expecting %s or %s or %s"));
        YYCASE_ (5, YY_("syntax error, unexpected %s, expecting %s or %s or %s or %s"));
#undef YYCASE_
      }

    std::string yyres;
    // Argument number.
    size_t yyi = 0;
    for (char const* yyp = yyformat; *yyp; ++yyp)
      if (yyp[0] == '%' && yyp[1] == 's' && yyi < yycount)
        {
          yyres += yytnamerr_ (yyarg[yyi++]);
          ++yyp;
        }
      else
        yyres += *yyp;
    return yyres;
  }


  const short parser::yypact_ninf_ = -287;

  const short parser::yytable_ninf_ = -192;

  const short
  parser::yypact_[] =
  {
      24,  -287,    38,    74,   348,   100,  -287,  -287,    79,    25,
     105,    14,  -287,  -287,   171,   109,  -287,  -287,  -287,  -287,
    -287,    54,  -287,   250,   124,  -287,    25,   349,   329,   300,
    -287,    73,     6,   132,   107,  -287,    25,   134,   142,   157,
    -287,   190,   105,  -287,   204,  -287,   196,   222,   250,  -287,
     303,   163,  -287,  -287,   234,   245,   250,   290,   266,  -287,
     214,    25,    25,  -287,  -287,  -287,  -287,   314,  -287,  -287,
     321,     8,   337,   105,  -287,  -287,   343,    42,    15,  -287,
      42,   349,   291,   331,  -287,  -287,   359,    97,    92,   378,
     379,   318,   250,   250,   360,  -287,   169,   390,   250,   147,
     361,  -287,   357,   362,  -287,  -287,   382,  -287,   366,   363,
     367,  -287,  -287,   398,  -287,  -287,  -287,  -287,   386,  -287,
    -287,  -287,   286,  -287,   372,   369,  -287,    42,    23,   372,
    -287,  -287,   195,   219,   373,  -287,  -287,  -287,   374,   371,
     375,  -287,   396,  -287,   372,  -287,  -287,  -287,   241,   250,
     376,  -287,   365,   377,   277,   246,   250,   380,  -287,   406,
    -287,   347,   411,   381,   414,   350,  -287,   286,   372,  -287,
     220,   281,  -287,   383,   196,  -287,   354,  -287,   365,   372,
       9,   384,   385,  -287,   387,   388,   389,   365,   175,   391,
     253,   393,  -287,  -287,   365,   365,  -287,  -287,    33,  -287,
     399,    31,  -287,  -287,   283,  -287,  -287,  -287,  -287,   250,
    -287,   280,   194,   400,  -287,    11,   394,   395,  -287,   400,
      45,   401,    19,   401,  -287,  -287,   250,  -287,  -287,  -287,
     397,   402,  -287,   403,  -287,  -287,  -287,   411,   356,  -287,
    -287,   365,  -287,  -287,  -287,   334,  -287,   372,   250,   404,
    -287,   416,   412,    -4,  -287,  -287,   415,  -287,   407,  -287,
    -287,   405,  -287,  -287,   408,  -287,   410,   365,   131,   419,
     253,  -287,  -287,   421,   160,   417,   106,  -287,  -287,   365,
      99,  -287,  -287,   250,   409,     9,   413,   418,   420,  -287,
     432,   422,  -287,  -287,   365,   397,  -287,   402,   423,   424,
    -287,   309,  -287,  -287,   171,   427,  -287,  -287,  -287,  -287,
    -287,  -287,   365,   320,  -287,  -287,  -287,   250,  -287,  -287,
    -287,  -287,  -287,  -287,   213,   429,   430,   426,   139,   352,
     372,   315,   428,   435,  -287,   431,   250,   436,   138,  -287,
     437,   319,  -287,  -287,   434,  -287,  -287,   189,   250,   229,
    -287,  -287,  -287,  -287,   227,   440,  -287,   308,   311,  -287,
     365,   438,  -287,  -287,  -287,  -287,  -287
  };

  const unsigned char
  parser::yydefact_[] =
  {
      12,    12,     0,     0,   110,     0,     1,     2,     0,     0,
       0,     0,     9,    11,    37,     0,     5,     7,     8,    10,
       6,   113,     3,     0,     0,   186,     0,    44,     0,    14,
      75,    76,     0,     0,    78,    46,     0,     0,     0,     0,
     112,     0,     0,   109,     0,   168,     0,     0,     0,   167,
      14,   159,    63,    64,     0,    66,     0,    94,    91,    65,
       0,     0,     0,    61,    62,    59,    60,   192,    57,    58,
       0,     0,     0,     0,    70,    13,     0,     0,     0,    79,
       0,    45,     0,     0,    12,    16,    19,    14,     0,     0,
       0,     0,     0,     0,     0,    68,     0,     0,     0,     0,
     175,    96,     0,   175,   185,    53,    52,    51,   188,     0,
       0,   187,    47,     0,    48,   132,    74,    77,    85,    86,
      87,    88,     0,    89,    14,    80,    84,     0,     0,    14,
      12,    12,   110,     0,     0,   111,   107,   108,     0,     0,
       0,   164,   166,   165,    14,   152,   153,   151,     0,   156,
     175,   149,   150,    98,    14,     0,   174,     0,    92,   174,
      93,     0,   192,     0,     0,     0,    72,     0,    14,    71,
     110,   110,    38,   186,    24,    18,     0,    21,    22,    14,
     115,     0,     0,    69,     0,     0,   175,   158,   174,     0,
       0,     0,    67,   184,   182,   181,   183,    95,     0,   191,
     189,     0,    90,    81,     0,    83,    73,    39,    36,     0,
      17,     0,     0,   123,   121,   119,     0,   175,   117,   123,
       0,   175,     0,   175,   160,   154,   174,   155,   148,   161,
     186,   100,   103,    99,    97,    49,    50,   192,     0,    54,
      82,    23,    20,   193,   194,    35,    15,    14,     0,   127,
     128,     0,   131,    14,   114,   120,     0,   170,   175,   172,
     174,     0,   180,   177,   175,   179,     0,   157,     0,     0,
       0,   190,    55,     0,    35,     0,   110,    28,    25,   122,
       0,   118,   129,     0,   142,     0,     0,   174,     0,   162,
     174,     0,   163,   105,   104,     0,   102,   101,     0,     0,
      26,     0,    34,    33,    41,     0,    30,    31,    32,   124,
     125,   126,   130,     0,   106,   135,   116,     0,   171,   169,
     178,   176,    56,    27,     0,     0,     0,     0,     0,     0,
     136,   175,     0,     0,    35,     0,     0,     0,     0,   144,
       0,     0,   138,   137,     0,    35,    35,   110,     0,   146,
     141,   134,   143,   140,     0,     0,   173,   110,   110,    42,
     145,     0,   133,   139,    43,    40,   147
  };

  const short
  parser::yypgoto_[] =
  {
    -287,  -287,   446,   -80,   -48,  -268,  -287,  -287,  -287,   238,
    -287,   177,    35,  -287,  -287,  -287,  -287,  -265,   148,   150,
     -21,   259,   305,  -260,  -287,  -287,   425,   461,   -73,   351,
    -157,  -253,  -287,  -287,  -287,  -287,   205,   207,  -246,  -287,
    -287,  -287,  -287,  -287,  -287,   192,   260,  -287,  -287,  -287,
    -286,  -287,  -287,   137,  -199,  -287,   292,  -287,   293,   -23,
    -287,  -287,   197,  -102,  -287,  -287,   191,  -287,  -287,    10,
    -287,  -159,  -206
  };

  const short
  parser::yydefgoto_[] =
  {
      -1,     2,     3,     4,    74,    12,    86,   134,   176,   177,
     246,   275,   276,    13,    14,   303,   304,    15,    37,    38,
      27,   114,    71,    16,    17,    29,    30,    79,   124,   125,
     126,    18,   102,   103,    19,   191,   231,   232,    20,   138,
      21,    43,    44,   216,   217,   218,   249,   281,   219,   284,
      75,   314,   315,   338,   339,   150,   151,   185,   186,    58,
     221,   258,   259,   157,   223,   264,   265,   100,    59,    51,
     109,   110,   277
  };

  const short
  parser::yytable_[] =
  {
      50,   160,    95,   200,   132,    60,   247,   129,   302,    25,
     205,   305,   213,   112,   250,    81,   306,    25,    25,    28,
      31,    34,    77,   307,   262,    91,    25,   329,    25,    72,
     308,   127,  -174,    99,   214,   238,    28,   235,     6,   135,
     106,   107,    34,   113,   343,   118,    28,   205,   189,    78,
     170,   171,    87,   215,   168,   251,     1,    32,   128,   263,
      26,    40,    41,   119,   120,   121,   128,   239,   113,   142,
     143,    28,    28,   152,     7,   154,   166,   122,   271,   302,
     256,   169,   305,    31,   227,   257,   123,   306,    34,   302,
     302,    76,   305,   305,   307,   136,   183,   306,   306,    42,
      22,   308,   309,   310,   307,   307,   192,   330,    25,   301,
     178,   308,   308,    23,   137,   254,    70,    24,     9,   261,
     206,   266,   340,   342,   311,    91,   187,    25,    52,    53,
      72,   212,   194,   195,    25,   355,   293,   -29,    34,   352,
      70,   335,   335,    39,    45,    46,    47,    54,    80,    55,
      70,    45,    46,    47,   243,   352,   288,   336,   336,    56,
      92,    93,   291,    57,   244,   152,    48,   187,    82,   351,
      49,   337,    25,   145,   146,   243,    83,    49,    25,   145,
     146,    35,    36,   141,   155,   244,   241,    84,   178,    45,
      46,    47,   301,    85,   147,    45,    46,    47,     8,   278,
     147,     9,    96,   267,   148,   285,    70,     9,   149,   243,
      48,    10,    11,    88,   149,    49,    25,    52,    53,   244,
     359,    49,   173,     8,   245,   279,   172,    61,    62,   344,
     335,    89,     9,    45,    46,    47,    10,    11,    55,    45,
     174,    47,    92,    93,    25,   294,   336,   267,    56,    25,
     105,   207,    57,    25,    48,   175,   230,    90,   362,    49,
     312,    45,    46,    47,   361,    49,    45,    46,    47,    97,
      45,    46,    47,    45,    46,    47,    48,   184,    98,    92,
      93,    48,   193,   173,     8,    48,   118,    49,    48,   118,
      92,    93,    49,     9,   331,   101,    49,    10,    11,    49,
      45,   174,    47,   104,   119,   120,   121,   119,   120,   121,
      72,   301,   208,   349,   301,    48,    92,    93,   108,   240,
       9,   130,   335,     9,   111,   360,    49,   123,    92,    93,
     123,    92,    93,    72,   243,   243,    72,    73,   336,   364,
     115,    94,   365,    23,   244,   244,   117,   324,    -4,   243,
     328,     8,   260,    72,   141,    63,    64,    65,    66,   244,
       9,   131,    61,    62,    10,    11,   274,   243,    67,   347,
      68,    69,    70,    63,    64,    65,    66,   244,    92,    93,
     357,   358,   341,   139,   140,   144,   203,   204,    68,    69,
     210,   211,   272,   273,   133,   153,    62,   158,   156,   159,
    -191,   162,   163,   161,   164,    72,   167,   179,   181,   180,
      93,   197,   182,   188,   190,   199,   196,   202,   201,   282,
     286,   209,   295,   220,   222,   298,   226,   224,   225,   234,
     252,   229,   253,   237,   248,   268,   283,   262,   260,   269,
     270,   289,   280,   313,   287,   290,   292,     5,   300,   242,
     317,   299,   325,   256,   326,   323,   334,   236,   345,   322,
     319,   327,   321,   332,   333,   346,   198,   350,   353,   348,
     356,   363,    33,   165,   366,   297,   296,   316,   354,   255,
     228,   320,     0,   233,   318,     0,     0,     0,     0,     0,
       0,     0,     0,     0,     0,     0,     0,     0,   116
  };

  const short
  parser::yycheck_[] =
  {
      23,   103,    50,   162,    84,    26,   212,    80,   276,     3,
     167,   276,     3,     5,     3,    36,   276,     3,     3,     9,
      10,    11,    16,   276,     5,    48,     3,   313,     3,    33,
     276,    16,    36,    56,    25,     4,    26,     4,     0,    87,
      61,    62,    32,    35,   330,     3,    36,   204,   150,    43,
     130,   131,    42,    44,   127,    44,    32,    43,    43,    40,
      35,     7,     8,    21,    22,    23,    43,    36,    35,    92,
      93,    61,    62,    96,     0,    98,   124,    35,   237,   347,
      35,   129,   347,    73,   186,    40,    44,   347,    78,   357,
     358,    18,   357,   358,   347,     3,   144,   357,   358,    45,
       0,   347,     3,     4,   357,   358,   154,   313,     3,     3,
     133,   357,   358,    34,    22,   217,    43,    38,    12,   221,
     168,   223,   328,   329,    25,   148,   149,     3,     4,     5,
      33,   179,   155,   156,     3,   341,     5,    31,   128,   338,
      43,     3,     3,    34,    20,    21,    22,    23,    16,    25,
      43,    20,    21,    22,    15,   354,   258,    19,    19,    35,
      13,    14,   264,    39,    25,   188,    35,   190,    34,    31,
      46,    32,     3,     4,     5,    15,    34,    46,     3,     4,
       5,    10,    11,    36,    37,    25,   209,    30,   211,    20,
      21,    22,     3,     3,    25,    20,    21,    22,     3,   247,
      25,    12,    39,   226,    35,   253,    43,    12,    39,    15,
      35,    16,    17,     9,    39,    46,     3,     4,     5,    25,
      31,    46,     3,     3,    30,   248,    31,    13,    14,   331,
       3,    35,    12,    20,    21,    22,    16,    17,    25,    20,
      21,    22,    13,    14,     3,   268,    19,   270,    35,     3,
      36,    31,    39,     3,    35,    36,     3,    35,    31,    46,
     283,    20,    21,    22,    35,    46,    20,    21,    22,    35,
      20,    21,    22,    20,    21,    22,    35,    36,    33,    13,
      14,    35,    36,     3,     3,    35,     3,    46,    35,     3,
      13,    14,    46,    12,   317,     5,    46,    16,    17,    46,
      20,    21,    22,    37,    21,    22,    23,    21,    22,    23,
      33,     3,    31,   336,     3,    35,    13,    14,     4,    36,
      12,    30,     3,    12,     3,   348,    46,    44,    13,    14,
      44,    13,    14,    33,    15,    15,    33,    37,    19,    31,
       3,    38,    31,    34,    25,    25,     3,    38,     0,    15,
      30,     3,    37,    33,    36,    26,    27,    28,    29,    25,
      12,    30,    13,    14,    16,    17,    32,    15,    39,   334,
      41,    42,    43,    26,    27,    28,    29,    25,    13,    14,
     345,   346,    30,     5,     5,    25,    36,    37,    41,    42,
      36,    37,    36,    37,    35,     5,    14,    40,    37,    37,
      34,    34,     4,    40,    18,    33,    37,    34,    37,    35,
      14,     5,    37,    37,    37,     4,    36,     3,    37,     3,
       5,    38,     3,    39,    39,     4,    37,    40,    40,    36,
      36,    40,    37,    34,    34,    38,    24,     5,    37,    37,
      37,    36,    38,    34,    37,    37,    36,     1,    31,   211,
      37,   274,   304,    35,   304,    31,    30,   198,    30,    36,
      40,    34,    40,    34,    34,    30,   161,    31,    31,    38,
      36,    31,    11,   122,    36,   270,   269,   285,   341,   219,
     188,   290,    -1,   190,   287,    -1,    -1,    -1,    -1,    -1,
      -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    73
  };

  const unsigned char
  parser::yystos_[] =
  {
       0,    32,    48,    49,    50,    49,     0,     0,     3,    12,
      16,    17,    52,    60,    61,    64,    70,    71,    78,    81,
      85,    87,     0,    34,    38,     3,    35,    67,   116,    72,
      73,   116,    43,    74,   116,    10,    11,    65,    66,    34,
       7,     8,    45,    88,    89,    20,    21,    22,    35,    46,
     106,   116,     4,     5,    23,    25,    35,    39,   106,   115,
      67,    13,    14,    26,    27,    28,    29,    39,    41,    42,
      43,    69,    33,    37,    51,    97,    18,    16,    43,    74,
      16,    67,    34,    34,    30,     3,    53,   116,     9,    35,
      35,   106,    13,    14,    38,    51,    39,    35,    33,   106,
     114,     5,    79,    80,    37,    36,    67,    67,     4,   117,
     118,     3,     5,    35,    68,     3,    73,     3,     3,    21,
      22,    23,    35,    44,    75,    76,    77,    16,    43,    75,
      30,    30,    50,    35,    54,    51,     3,    22,    86,     5,
       5,    36,   106,   106,    25,     4,     5,    25,    35,    39,
     102,   103,   106,     5,   106,    37,    37,   110,    40,    37,
     110,    40,    34,     4,    18,    76,    51,    37,    75,    51,
      50,    50,    31,     3,    21,    36,    55,    56,   106,    34,
      35,    37,    37,    51,    36,   104,   105,   106,    37,   110,
      37,    82,    51,    36,   106,   106,    36,     5,    69,     4,
     118,    37,     3,    36,    37,    77,    51,    31,    31,    38,
      36,    37,    51,     3,    25,    44,    90,    91,    92,    95,
      39,   107,    39,   111,    40,    40,    37,   110,   103,    40,
       3,    83,    84,   105,    36,     4,    68,    34,     4,    36,
      36,   106,    56,    15,    25,    30,    57,   119,    34,    93,
       3,    44,    36,    37,   110,    93,    35,    40,   108,   109,
      37,   110,     5,    40,   112,   113,   110,   106,    38,    37,
      37,   118,    36,    37,    32,    58,    59,   119,    51,   106,
      38,    94,     3,    24,    96,    51,     5,    37,   110,    36,
      37,   110,    36,     5,   106,     3,    84,    83,     4,    58,
      31,     3,    52,    62,    63,    64,    70,    78,    85,     3,
       4,    25,   106,    34,    98,    99,    92,    37,   109,    40,
     113,    40,    36,    31,    38,    65,    66,    34,    30,    97,
     119,   106,    34,    34,    30,     3,    19,    32,   100,   101,
     119,    30,   119,    97,   110,    30,    30,    59,    38,   106,
      31,    31,   101,    31,   100,   119,    36,    59,    59,    31,
     106,    35,    31,    31,    31,    31,    36
  };

  const unsigned char
  parser::yyr1_[] =
  {
       0,    47,    48,    48,    49,    50,    50,    50,    50,    50,
      50,    50,    50,    51,    51,    52,    53,    54,    54,    54,
      55,    55,    56,    56,    56,    57,    57,    57,    58,    58,
      59,    59,    59,    59,    59,    59,    60,    60,    61,    61,
      62,    62,    63,    63,    64,    65,    66,    67,    67,    67,
      67,    67,    67,    67,    68,    68,    68,    69,    69,    69,
      69,    69,    69,    70,    70,    70,    70,    70,    70,    70,
      71,    71,    71,    71,    72,    72,    73,    73,    74,    74,
      75,    75,    75,    76,    76,    77,    77,    77,    77,    77,
      77,    78,    78,    79,    79,    80,    80,    81,    82,    82,
      82,    82,    83,    83,    84,    84,    85,    86,    86,    87,
      87,    88,    89,    89,    90,    90,    91,    91,    92,    92,
      92,    92,    93,    93,    94,    94,    94,    94,    95,    95,
      96,    96,    97,    98,    98,    98,    99,    99,    99,    99,
      99,    99,    99,   100,   100,   101,   101,   101,   102,   102,
     103,   103,   103,   103,   103,   104,   104,   105,   105,   106,
     106,   106,   106,   106,   106,   106,   106,   106,   106,   107,
     107,   108,   108,   109,   110,   110,   111,   111,   112,   112,
     113,   114,   114,   115,   115,   115,   116,   116,   117,   117,
     117,   118,   118,   119,   119
  };

  const unsigned char
  parser::yyr2_[] =
  {
       0,     2,     2,     3,     1,     2,     2,     2,     2,     2,
       2,     2,     0,     1,     0,     7,     1,     3,     2,     0,
       3,     1,     1,     3,     1,     2,     3,     4,     1,     1,
       2,     2,     2,     2,     2,     0,     6,     1,     5,     6,
       6,     1,     5,     6,     2,     2,     1,     3,     3,     6,
       6,     3,     3,     3,     4,     5,     7,     1,     1,     1,
       1,     1,     1,     3,     3,     3,     3,     6,     4,     6,
       3,     5,     5,     6,     3,     1,     1,     3,     1,     2,
       1,     3,     4,     3,     1,     1,     1,     1,     1,     1,
       3,     3,     5,     2,     0,     3,     1,     7,     0,     2,
       2,     4,     3,     1,     3,     3,     9,     1,     1,     2,
       0,     3,     1,     0,     2,     0,     4,     1,     3,     1,
       2,     1,     2,     0,     2,     2,     2,     0,     2,     3,
       2,     0,     2,     5,     4,     1,     2,     3,     3,     5,
       4,     4,     0,     2,     1,     3,     2,     4,     3,     1,
       1,     1,     1,     1,     3,     2,     0,     3,     1,     1,
       5,     5,     7,     7,     3,     3,     3,     1,     1,     4,
       2,     3,     1,     6,     1,     0,     4,     2,     3,     1,
       1,     3,     3,     4,     4,     2,     1,     3,     1,     3,
       5,     1,     0,     1,     1
  };



  // YYTNAME[SYMBOL-NUM] -- String name of the symbol SYMBOL-NUM.
  // First, the terminals, then, starting at \a yyntokens_, nonterminals.
  const char*
  const parser::yytname_[] =
  {
  "\"end of file\"", "error", "$undefined", "NAME", "NUMBER", "STRING",
  "LEXERROR", "ASYNC", "CLASS", "DEF", "ELSE", "ELIF", "IF", "OR", "AND",
  "PASS", "IMPORT", "FROM", "AS", "RAISE", "NOTHING", "NAMEDTUPLE",
  "COLL_NAMEDTUPLE", "TYPEVAR", "ARROW", "ELLIPSIS", "EQ", "NE", "LE",
  "GE", "INDENT", "DEDENT", "TRIPLEQUOTED", "TYPECOMMENT", "':'", "'('",
  "')'", "','", "'='", "'['", "']'", "'<'", "'>'", "'.'", "'*'", "'@'",
  "'?'", "$accept", "start", "unit", "alldefs", "maybe_type_ignore",
  "classdef", "class_name", "parents", "parent_list", "parent",
  "maybe_class_funcs", "class_funcs", "funcdefs", "if_stmt",
  "if_and_elifs", "class_if_stmt", "class_if_and_elifs", "if_cond",
  "elif_cond", "else_cond", "condition", "version_tuple", "condition_op",
  "constantdef", "importdef", "import_items", "import_item", "import_name",
  "from_list", "from_items", "from_item", "alias_or_constant",
  "maybe_string_list", "string_list", "typevardef", "typevar_args",
  "typevar_kwargs", "typevar_kwarg", "funcdef", "funcname", "decorators",
  "decorator", "maybe_async", "params", "param_list", "param",
  "param_type", "param_default", "param_star_name", "return", "typeignore",
  "maybe_body", "empty_body", "body", "body_stmt", "type_parameters",
  "type_parameter", "maybe_type_list", "type_list", "type",
  "named_tuple_fields", "named_tuple_field_list", "named_tuple_field",
  "maybe_comma", "coll_named_tuple_fields", "coll_named_tuple_field_list",
  "coll_named_tuple_field", "type_tuple_elements", "type_tuple_literal",
  "dotted_name", "getitem_key", "maybe_number", "pass_or_ellipsis", YY_NULLPTR
  };

#if PYTYPEDEBUG
  const unsigned short
  parser::yyrline_[] =
  {
       0,   134,   134,   135,   139,   143,   144,   145,   146,   152,
     153,   154,   159,   163,   164,   171,   181,   192,   193,   194,
     198,   199,   203,   204,   205,   209,   210,   211,   215,   216,
     220,   221,   226,   227,   232,   233,   238,   241,   246,   250,
     269,   272,   277,   281,   293,   297,   301,   305,   308,   311,
     314,   317,   318,   319,   324,   325,   326,   332,   333,   334,
     335,   336,   337,   341,   345,   349,   353,   357,   361,   365,
     372,   376,   380,   386,   395,   396,   400,   401,   406,   407,
     414,   415,   416,   420,   421,   425,   426,   429,   432,   435,
     438,   442,   443,   447,   448,   452,   453,   457,   464,   465,
     466,   467,   471,   472,   476,   478,   482,   499,   500,   504,
     505,   509,   513,   514,   518,   519,   531,   532,   536,   537,
     538,   539,   543,   544,   548,   549,   550,   551,   555,   556,
     560,   561,   565,   569,   570,   571,   575,   576,   577,   578,
     579,   580,   581,   585,   586,   590,   591,   592,   596,   597,
     601,   602,   604,   605,   607,   614,   615,   619,   620,   624,
     628,   632,   636,   640,   644,   645,   646,   647,   648,   652,
     653,   657,   658,   662,   666,   667,   671,   672,   676,   679,
     683,   690,   691,   700,   705,   711,   718,   719,   733,   734,
     739,   747,   748,   752,   753
  };

  // Print the state stack on the debug stream.
  void
  parser::yystack_print_ ()
  {
    *yycdebug_ << "Stack now";
    for (stack_type::const_iterator
           i = yystack_.begin (),
           i_end = yystack_.end ();
         i != i_end; ++i)
      *yycdebug_ << ' ' << i->state;
    *yycdebug_ << '\n';
  }

  // Report on the debug stream that the rule \a yyrule is going to be reduced.
  void
  parser::yy_reduce_print_ (int yyrule)
  {
    unsigned yylno = yyrline_[yyrule];
    int yynrhs = yyr2_[yyrule];
    // Print the symbols being reduced, and their result.
    *yycdebug_ << "Reducing stack by rule " << yyrule - 1
               << " (line " << yylno << "):\n";
    // The symbols being reduced.
    for (int yyi = 0; yyi < yynrhs; yyi++)
      YY_SYMBOL_PRINT ("   $" << yyi + 1 << " =",
                       yystack_[(yynrhs) - (yyi + 1)]);
  }
#endif // PYTYPEDEBUG

  parser::token_number_type
  parser::yytranslate_ (int t)
  {
    // YYTRANSLATE[TOKEN-NUM] -- Symbol number corresponding to
    // TOKEN-NUM as returned by yylex.
    static
    const token_number_type
    translate_table[] =
    {
       0,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
      35,    36,    44,     2,    37,     2,    43,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,    34,     2,
      41,    38,    42,    46,    45,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,    39,     2,    40,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     2,     2,     2,     2,
       2,     2,     2,     2,     2,     2,     1,     2,     3,     4,
       5,     6,     7,     8,     9,    10,    11,    12,    13,    14,
      15,    16,    17,    18,    19,    20,    21,    22,    23,    24,
      25,    26,    27,    28,    29,    30,    31,    32,    33
    };
    const unsigned user_token_number_max_ = 288;
    const token_number_type undef_token_ = 2;

    if (static_cast<int> (t) <= yyeof_)
      return yyeof_;
    else if (static_cast<unsigned> (t) <= user_token_number_max_)
      return translate_table[t];
    else
      return undef_token_;
  }

#line 17 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"
} // pytype
#line 3047 "/usr/local/google/home/rechen/pytype/out/pytype/pyi/parser.tab.cc"

#line 756 "/usr/local/google/home/rechen/pytype/pytype/pyi/parser.yy"


void pytype::parser::error(const location& loc, const std::string& msg) {
  ctx->SetErrorLocation(loc);
  pytype::Lexer* lexer = pytypeget_extra(scanner);
  if (lexer->error_message_) {
    PyErr_SetObject(ctx->Value(pytype::kParseError), lexer->error_message_);
  } else {
    PyErr_SetString(ctx->Value(pytype::kParseError), msg.c_str());
  }
}

namespace {

PyObject* StartList(PyObject* item) {
  return Py_BuildValue("[N]", item);
}

PyObject* AppendList(PyObject* list, PyObject* item) {
  PyList_Append(list, item);
  Py_DECREF(item);
  return list;
}

PyObject* ExtendList(PyObject* dst, PyObject* src) {
  // Add items from src to dst (both of which must be lists) and return src.
  // Borrows the reference to src.
  Py_ssize_t count = PyList_Size(src);
  for (Py_ssize_t i=0; i < count; ++i) {
    PyList_Append(dst, PyList_GetItem(src, i));
  }
  Py_DECREF(src);
  return dst;
}

}  // end namespace
