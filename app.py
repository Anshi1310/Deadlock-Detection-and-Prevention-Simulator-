from flask import Flask, render_template, request
import copy

app = Flask(__name__)

class DeadlockSimulator:
    def __init__(self, processes, resources, available, max_matrix, allocation):
        self.processes = processes
        self.resources = resources
        self.available = available
        self.max_matrix = max_matrix
        self.allocation = allocation
        self.need = self.calculate_need()
        self.steps = []
        self.validation_error = self.validate_allocation()

    def validate_allocation(self):
        for i in range(self.processes):
            for j in range(self.resources):
                if self.allocation[i][j] > self.max_matrix[i][j]:
                    return f"Error: Process P{i} has allocated resources ({self.allocation[i][j]}) greater than its maximum need ({self.max_matrix[i][j]}) for resource R{j}"
        return None

    def calculate_need(self):
        return [[self.max_matrix[i][j] - self.allocation[i][j] for j in range(self.resources)] for i in range(self.processes)]

    def is_safe_state(self):
        work = self.available[:]
        finish = [False] * self.processes
        safe_seq = []
        self.steps = []

        while True:
            found = False
            for i in range(self.processes):
                if not finish[i]:
                    can_allocate = all(self.need[i][j] <= work[j] for j in range(self.resources))
                    label = f"Checking if P{i} can proceed"
                    self.steps.append({
                        'process': f'P{i}',
                        'need': self.need[i][:],
                        'work': work[:],
                        'can_allocate': can_allocate,
                        'action': 'Checking if process can be allocated resources',
                        'label': label
                    })
                    if can_allocate:
                        for j in range(self.resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
                        safe_seq.append(f"P{i}")
                        found = True
                        label = f"Allocating resources to P{i} and marking as finished"
                        self.steps.append({
                            'process': f'P{i}',
                            'work': work[:],
                            'action': 'Resources allocated and process completed',
                            'label': label
                        })
            if not found:
                self.steps.append({
                    'process': '-',
                    'work': work[:],
                    'action': 'No process can proceed, ending check',
                    'label': 'No process can proceed, ending check'
                })
                break
        return all(finish), safe_seq

    def generate_wait_for_graph(self):
        wfg = {}
        for i in range(self.processes):
            wfg[f"P{i}"] = []
            for j in range(self.processes):
                if i != j:
                    can_proceed = all(self.need[i][k] <= self.available[k] + self.allocation[j][k] for k in range(self.resources))
                    if not can_proceed:
                        wfg[f"P{i}"].append(f"P{j}")
        return wfg

    def detect_deadlock(self):
        is_safe, safe_seq = self.is_safe_state()
        deadlocked = []
        if not is_safe:
            work = self.available[:]
            finish = [False] * self.processes
            for _ in range(self.processes):
                for i in range(self.processes):
                    if not finish[i] and all(self.need[i][j] <= work[j] for j in range(self.resources)):
                        for j in range(self.resources):
                            work[j] += self.allocation[i][j]
                        finish[i] = True
            deadlocked = [f"P{i}" for i, done in enumerate(finish) if not done]
        return not is_safe, self.need, safe_seq, deadlocked

    def prevent_request(self, request_process, request):
        if request_process < 0 or request_process >= self.processes:
            return False, "Request denied: Invalid process index.", [], []
        if len(request) != self.resources:
            return False, "Request denied: Request vector length must match number of resources.", [], []
        for i in range(self.resources):
            if request[i] > self.available[i]:
                return False, f"Request denied: exceeds available resources. Available: {self.available[i]}, Requested: {request[i]}", [], []
            if request[i] > self.need[request_process][i]:
                return False, f"Request denied: exceeds maximum need for process P{request_process}.", [], []
        new_allocation = copy.deepcopy(self.allocation)
        new_available = self.available[:]
        for i in range(self.resources):
            new_allocation[request_process][i] += request[i]
            new_available[i] -= request[i]
        new_simulator = DeadlockSimulator(self.processes, self.resources, new_available, self.max_matrix, new_allocation)
        is_safe, safe_seq = new_simulator.is_safe_state()
        return is_safe, (f"Request can be granted safely. Safe Sequence: {' → '.join(safe_seq)}" if is_safe else "Request would lead to unsafe state. Request denied."), safe_seq, new_simulator.steps

@app.route('/', methods=['GET', 'POST'])
def index():
    form_data = {
        'processes': '',
        'resources': '',
        'available': '',
        'max_matrix': [],
        'allocation': [],
        'request_process': '',
        'request': '',
        'mode': 'detect'
    }
    result = ""
    safe_seq = []
    deadlock = False
    prevention_result = ""
    steps = []
    wfg = {}
    need = []
    deadlocked = []

    if request.method == 'POST':
        try:
            processes = request.form.get('processes', '')
            resources = request.form.get('resources', '')
            available = request.form.get('available', '')
            mode = request.form.get('mode', 'detect')
            form_data.update({'processes': processes, 'resources': resources, 'available': available, 'mode': mode})
            if not processes or not resources:
                return render_template('index.html', error="Number of processes and resources must be provided.", form_data=form_data)
            processes = int(processes)
            resources = int(resources)
            available_list = list(map(int, available.split()))
            max_matrix = []
            allocation = []
            for i in range(processes):
                max_row = []
                alloc_row = []
                for j in range(resources):
                    max_val = request.form.get(f'max_{i}_{j}', '')
                    alloc_val = request.form.get(f'allocation_{i}_{j}', '')
                    max_row.append(max_val)
                    alloc_row.append(alloc_val)
                max_matrix.append(max_row)
                allocation.append(alloc_row)
            form_data['max_matrix'] = max_matrix
            form_data['allocation'] = allocation
            max_matrix_int = [[int(cell) for cell in row] for row in max_matrix]
            allocation_int = [[int(cell) for cell in row] for row in allocation]
            request_process = request.form.get('request_process', '')
            request_vector = request.form.get('request', '')
            form_data['request_process'] = request_process
            form_data['request'] = request_vector

            simulator = DeadlockSimulator(processes, resources, available_list, max_matrix_int, allocation_int)
            
            # Check for allocation validation error
            if simulator.validation_error:
                return render_template('index.html', error=simulator.validation_error, form_data=form_data)

            need = simulator.need
            wfg = simulator.generate_wait_for_graph()

            if mode == 'detect':
                deadlock, need, safe_seq, deadlocked = simulator.detect_deadlock()
                result = "System is in a Safe State." if not deadlock else f"System is in an Unsafe State. Deadlocked processes: {', '.join(deadlocked)}"
                steps = simulator.steps
            elif mode == 'prevent':
                if request_process == '' or request_vector == '':
                    return render_template('index.html', error="Requesting process and request vector must be provided.", form_data=form_data)
                request_process_int = int(request_process)
                request_vector_list = list(map(int, request_vector.split()))
                granted, prevention_result, safe_seq, steps = simulator.prevent_request(request_process_int, request_vector_list)
                result = "Safe State after Request." if granted else "Unsafe State after Request."
                wfg = simulator.generate_wait_for_graph()
            return render_template('index.html',
                                   result=result,
                                   need=need,
                                   safe_seq=safe_seq,
                                   deadlock=deadlock,
                                   wfg=wfg,
                                   mode=mode,
                                   prevention_result=prevention_result,
                                   steps=steps,
                                   form_data=form_data,
                                   deadlocked=deadlocked)
        except Exception as e:
            return render_template('index.html', error=f"An error occurred: {str(e)}", form_data=form_data)
    return render_template('index.html', form_data=form_data)

if __name__== '__main__':
    app.run(debug=True, port=5050)