function y_nplus1 = fun_rk4(handle_f,y_n,dt,t)

if nargin==3
    k1 = dt*feval(handle_f,y_n);
    k2 = dt*feval(handle_f,y_n+k1/2);
    k3 = dt*feval(handle_f,y_n+k2/2);
    k4 = dt*feval(handle_f,y_n+k3);
else
    k1 = dt*feval(handle_f,y_n,t);
    k2 = dt*feval(handle_f,y_n+k1/2,t);
    k3 = dt*feval(handle_f,y_n+k2/2,t);
    k4 = dt*feval(handle_f,y_n+k3,t);
end

y_nplus1 = y_n + (k1+2*k2+2*k3+k4)/6;