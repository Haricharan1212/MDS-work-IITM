function y_corrector = fun_Huen(handle_f,y_n,dt,t)

if nargin==3
    y_predictor = y_n + dt*feval(handle_f,y_n);
    y_corrector = y_n + dt/2*(feval(handle_f,y_n) + feval(handle_f,y_predictor));
else
    y_predictor = y_n + dt*feval(handle_f,y_n,t);
    y_corrector = y_n + dt/2*(feval(handle_f,y_n,t) + feval(handle_f,y_predictor,t));
end