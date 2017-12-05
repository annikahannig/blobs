#!/usr/bin/env escript

-module(marching_square).



%%---------------------------------------------------------
%% Render distance field using marching square algorithm
%%---------------------------------------------------------

sample_box(X, Y, Field) ->
    {sample_at(X, Y, Field),     sample_at(X + 1, Y, Field),
     sample_at(X, Y + 1, Field), sample_at(X + 1, Y + 1, Field)}.


sample_at(X, Y, Field) ->
    Y1 = clamp_value(1, length(Field), Y),
    Row = lists:nth(Y1, Field),
    X1 = clamp_value(1, length(Row), X),
    
    lists:nth(X1, Row).


clamp_value(Min, _, V) when V < Min -> Min;
clamp_value(_, Max, V) when V > Max -> Max;
clamp_value(_, _, V) -> V.


apply_threshold(Th, V) when V >= Th -> true;
apply_threshold(_, _) -> false.

apply_box_threshold(Th, Box) ->
    {Tl, Tr, Bl, Br} = Box,

    {apply_threshold(Th, Tl), apply_threshold(Th, Tr),
     apply_threshold(Th, Bl), apply_threshold(Th, Br)}.
    


shade_box_lines({false, false, false, false}) -> "_";
shade_box_lines({true,  true,  true,  true})  -> " ";
shade_box_lines({true,  false, true,  false}) -> "|";
shade_box_lines({false, true,  false, true})  -> "|";
shade_box_lines({false, false, true,  true})  -> "_";
shade_box_lines({true,  true,  false, false}) -> "-";
shade_box_lines({false, true,  true,  true})  -> "/";
shade_box_lines({true,  true,  true,  false}) -> "/";
shade_box_lines({true,  true,  false, true})  -> "\\";
shade_box_lines({true,  false, true,  true})  -> "\\";
shade_box_lines(_) -> "_".


shade_field(Hres, Vres, Shader, Field) ->
    [[Shader(apply_box_threshold(0.03, sample_box(X, Y, Field))) 
      || X <- lists:seq(1, Hres)]
     || Y <- lists:seq(1, Vres)].


% Render shader ouput
output_field([]) ->
    io:format("~n");

output_field([Row | Field]) ->
    io:format("~s~n", [string:join(Row, "")]),
    output_field(Field).


%%---------------------------------------------------------
%% Implementation of distance field
%%---------------------------------------------------------

balls(T) ->
    [{23 + 15 * math:cos(T), 10 + 10 * math:sin(0.75 * T)},
     {40 + 8  * math:cos(T + 15), 5 + 6 * math:sin(T)},
     {60 + 15 * math:sin(T), 18 + 5 * math:cos(T)},
     {30 + 0 * math:cos(T), 20 + 0 * math:sin(T)}].

balls_field(X, Y, T) ->
    Q = {X, Y},
    lists:sum([dist_gradient(Q, P) || P <- balls(T)]).


dist_gradient({X0, Y0}, {X1, Y1})
        when (X0 == X1) and (Y0 == Y1)
    -> 1.0;

dist_gradient({X0, Y0}, {X1, Y1}) ->
    X = X1 - X0,
    Y = Y1 - Y0,
    1.0 / (X*X + Y*Y).


dfield(Hres, Vres, Fn, T) ->
    [[Fn(X, Y, T) || X <- lists:seq(1, Hres)]
     || Y <- lists:seq(1, Vres)].


render_frame(T) ->
    Hres = 80,
    Vres = 30,
    Field = dfield(Hres, Vres, fun(X, Y, Tf) -> balls_field(X, Y, Tf) end, T),
    Shaded = shade_field(Hres, Vres, fun(Box) -> shade_box_lines(Box) end, Field),

    io:format("~c[2J", [27]),
    output_field(Shaded),

    render_frame(T + 0.1).


main(_) ->
    render_frame(0).

