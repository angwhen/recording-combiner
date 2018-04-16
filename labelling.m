filename = 'yosemite.txt';
delimiterIn = ' ';
my_data = importdata(filename,delimiterIn);
my_data(:,4) = []; %remove last column about light

% filter based on time
start_time = 0.0001;
end_time = 0.0002;
row_idx = (my_data(:,1) >= start_time);
A = my_data(row_idx,:);
row_idx = (my_data(:,1) <= end_time);
A = A(row_idx,:);

%display
scatter(A(:,2),A(:,3))

%get bounding box
h = impoly();
nodes = getPosition(h);
disp(nodes) % list of vertices on image i guess?
