dataloc = '~/Downloads/two-axis-3/'
posS = 20.5;
posE = 21.5;
n = 50;

bpaom = fdesign.bandpass('Fst1,Fp1,Fp2,Fst2,Ast1,Ap,Ast2',0.45,0.475,0.525,0.55,60,1,60);
Hbpaom = design(bpaom, 'equiripple');

% all_envs = [];
% all_env_primes = [];
% AllAfs = [];
% all_p_double_primes = [];

fwhm = zeros(n,1);
max_pos = zeros(n,1);
max_pos_prime = zeros(n,1);

ds = [];

for i = 0:(n-1)
    disp(['Number ' num2str(i)])
    A = load([dataloc 'data' num2str(i) '.dat']);
    pos = csvread([dataloc 'z_position_list' num2str(i) '.csv']);
    t = pos(:,1);
    p = pos(:,2);

    % correct zero point
    A = A - 4096/2;
    
    Af = filter(Hbpaom, A);
    AllAfs = [AllAfs, Af];
    env = abs(hilbert(Af));
    
    t = t * 2; % convert microseconds to samples
    p = p(t > 0); 
    t = t(t > 0);
    
    t_prime = t(1):t(end);
    p_prime = interp1(t, p, t_prime);
    dp_prime = diff(p_prime);
    
    % directionality issue
    if (posS < posE)
        ind = find(dp_prime <= 0);
    else
        ind = find(dp_prime >= 0);
    end
    
    if (numel(ind) ~= 0)
        non_monotonic = ind(1);
    else
        non_monotonic = length(p_prime);
    end
    
    p_prime = p_prime(1:non_monotonic);
    
    p_double_prime = linspace(posS, posE, 1e5);
    env_prime = interp1(p_prime, env(t(1):t_prime(non_monotonic)), ...
        p_double_prime, 'spline', 0);
    
    % all_envs = [all_envs, env];
    % all_env_primes = [all_env_primes env_prime'];

    [~, center] = max(env);
    [~, center_interp] = max(env_prime)
    center_p = p_double_prime(center_interp)

    max_pos(i+1) = center;
    max_pos_prime(i+1) = center_p;
end
