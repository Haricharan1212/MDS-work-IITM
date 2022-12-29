function y_n_plus1 = fun_explicitEuler(handle_f,y_n,dt,t)

%%% nargin = num of arguments passed to function

if nargin==3 
    y_n_plus1 = y_n + dt*feval(handle_f,y_n);
else
    y_n_plus1 = y_n + dt*feval(handle_f,y_n,t);
end