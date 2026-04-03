import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Original colors
COLORS = {0: 'white', 1: '#ff6961', 2: '#2f2f2f'}
AGENT_COLOR = '#0000ff'

_selected_option = None


# ==========================================
# Grid World (original logic, clean visuals)
# ==========================================
class GridWorld:
    def __init__(self, rows=5, cols=5):
        self.rows = rows
        self.cols = cols
        self.grid = [[0 for _ in range(cols)] for _ in range(rows)]

        # Patients
        for _ in range(4):
            while True:
                r, c = random.randint(0, rows-1), random.randint(0, cols-1)
                if self.grid[r][c] == 0:
                    self.grid[r][c] = 1
                    break

        # Obstacles (cars)
        for _ in range(3):
            while True:
                r, c = random.randint(0, rows-1), random.randint(0, cols-1)
                if self.grid[r][c] == 0:
                    self.grid[r][c] = 2
                    break

        self.fig, self.ax = None, None
        self.agent_r, self.agent_c = 0, 0
        self.agent_type = ""
        self.steps = 0
        self.rescued = 0

    def copy_layout(self):
        return [row[:] for row in self.grid]

    def load_layout(self, layout):
        self.grid = [row[:] for row in layout]

    def is_valid(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols and self.grid[r][c] != 2

    def setup_plot(self):
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.fig.patch.set_facecolor('#1e1e1e')
        self.ax.set_facecolor('#2d2d2d')

    def draw_grid(self, title=""):
        self.ax.clear()
        self.ax.set_xlim(-0.5, self.cols-0.5)
        self.ax.set_ylim(-0.5, self.rows-0.5)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.2)
        self.ax.set_axis_off()
        self.ax.set_title(title, color='white', fontsize=14, pad=20, fontweight='bold')

        # Draw cells (original colors)
        for r in range(self.rows):
            for c in range(self.cols):
                rect = patches.Rectangle((c-0.5, r-0.5), 1, 1,
                                         edgecolor='black',
                                         facecolor=COLORS[self.grid[r][c]])
                self.ax.add_patch(rect)

        # Agent circle (original)
        circle = patches.Circle((self.agent_c, self.agent_r), 0.3, color=AGENT_COLOR)
        self.ax.add_patch(circle)

        # Stats panel (clean, no broken progress bar)
        stats_text = f"{self.agent_type}\nSteps: {self.steps}\nRescued: {self.rescued}/4"
        self.ax.text(0.02, 0.98, stats_text,
                     transform=self.ax.transAxes,
                     verticalalignment='top',
                     fontsize=11,
                     color='white',
                     fontweight='bold',
                     bbox=dict(facecolor='#2d2d2d', alpha=0.9,
                               edgecolor='#4a90e2', linewidth=2,
                               boxstyle='round,pad=0.5'))

        plt.pause(0.15)


# ==========================================
# Menu (clean as requested)
# ==========================================
def draw_menu(world, title, options, disabled):
    world.ax.clear()
    world.ax.set_axis_off()
    world.ax.set_facecolor('#1e1e1e')
    world.ax.set_title(title, color='white', fontsize=16, pad=30, fontweight='bold')
    
    # Draw border
    rect = patches.Rectangle((-0.5, -0.5), world.cols, world.rows, 
                            linewidth=2, edgecolor='#4a90e2', 
                            facecolor='none')
    world.ax.add_patch(rect)
    
    y_pos = 0.65
    for i, opt in enumerate(options):
        if i in disabled:
            color = '#666666'
            status = " ✓ COMPLETED"
        else:
            color = '#4a90e2'
            status = ""
        
        world.ax.text(0.2, y_pos - i*0.12, f"{opt}{status}", 
                     fontsize=13, color=color, fontweight='bold')
    
    world.ax.text(0.2, 0.25, "Press 1, 2, or 3 to select agent", 
                 fontsize=11, color='white', alpha=0.8)
    world.ax.text(0.2, 0.15, "Each agent will run 50 steps max", 
                 fontsize=10, color='gray', alpha=0.6)
    
    plt.pause(0.1)


def on_key(event):
    global _selected_option
    if event.key in ['1', '2', '3']:
        _selected_option = int(event.key) - 1


# ==========================================
# Agents (EXACT original logic)
# ==========================================
class SimpleReflexRescueAgent:
    def __init__(self, grid):
        self.grid = grid
        self.r, self.c = 0, 0
        self.rescued = 0

    def act(self):
        if self.grid.grid[self.r][self.c] == 1:
            self.grid.grid[self.r][self.c] = 0
            self.rescued += 1

        for dr, dc in random.sample([(0,1),(1,0),(0,-1),(-1,0)], 4):
            nr, nc = self.r+dr, self.c+dc
            if self.grid.is_valid(nr, nc):
                self.r, self.c = nr, nc
                break

        self.update()

    def update(self):
        self.grid.steps += 1
        self.grid.rescued = self.rescued
        self.grid.agent_r = self.r
        self.grid.agent_c = self.c
        self.grid.draw_grid("Simple Reflex Agent")


class ModelBasedReflexRescueAgent:
    def __init__(self, grid):
        self.grid = grid
        self.r, self.c = 0, 0
        self.rescued = 0
        self.visited = set()

    def act(self):
        self.visited.add((self.r, self.c))

        if self.grid.grid[self.r][self.c] == 1:
            self.grid.grid[self.r][self.c] = 0
            self.rescued += 1

        for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
            nr, nc = self.r+dr, self.c+dc
            if self.grid.is_valid(nr, nc) and (nr, nc) not in self.visited:
                self.r, self.c = nr, nc
                break
        else:
            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                nr, nc = self.r+dr, self.c+dc
                if self.grid.is_valid(nr, nc):
                    self.r, self.c = nr, nc
                    break

        self.update()

    def update(self):
        self.grid.steps += 1
        self.grid.rescued = self.rescued
        self.grid.agent_r = self.r
        self.grid.agent_c = self.c
        self.grid.draw_grid("Model-Based Agent")


class GoalBasedRescueAgent:
    def __init__(self, grid):
        self.grid = grid
        self.r, self.c = 0, 0
        self.rescued = 0

    def find_patients(self):
        return [(r,c) for r in range(self.grid.rows)
                for c in range(self.grid.cols)
                if self.grid.grid[r][c] == 1]

    def act(self):
        if self.grid.grid[self.r][self.c] == 1:
            self.grid.grid[self.r][self.c] = 0
            self.rescued += 1
            self.update()
            return

        patients = self.find_patients()

        if not patients:
            self.update()
            return

        target = min(patients, key=lambda p: abs(p[0]-self.r)+abs(p[1]-self.c))

        moved = False

        if target[0] > self.r and self.grid.is_valid(self.r+1, self.c):
            self.r += 1
            moved = True
        elif target[0] < self.r and self.grid.is_valid(self.r-1, self.c):
            self.r -= 1
            moved = True
        elif target[1] > self.c and self.grid.is_valid(self.r, self.c+1):
            self.c += 1
            moved = True
        elif target[1] < self.c and self.grid.is_valid(self.r, self.c-1):
            self.c -= 1
            moved = True

        if not moved:
            for dr, dc in [(0,1),(1,0),(0,-1),(-1,0)]:
                nr, nc = self.r + dr, self.c + dc
                if self.grid.is_valid(nr, nc):
                    self.r, self.c = nr, nc
                    break

        self.update()

    def update(self):
        self.grid.steps += 1
        self.grid.rescued = self.rescued
        self.grid.agent_r = self.r
        self.grid.agent_c = self.c
        self.grid.draw_grid("Goal-Based Agent")


# ==========================================
# Completion Page (NEW)
# ==========================================
def show_completion_page(world):
    world.ax.clear()
    world.ax.set_axis_off()
    world.ax.set_facecolor('#1e1e1e')
    world.ax.set_title("Mission Complete", color='white', fontsize=18, pad=40, fontweight='bold')
    
    # Draw decorative border
    rect = patches.Rectangle((-0.5, -0.5), world.cols, world.rows, 
                            linewidth=3, edgecolor='#4a90e2', 
                            facecolor='none')
    world.ax.add_patch(rect)
    
    # Completion message
    message = """
    ✅ All agents have finished execution!
    
    Three different rescue strategies were tested:
    • Simple Reflex Agent
    • Model-Based Agent  
    • Goal-Based Agent
    
    Click the dashboard window to view detailed
    performance comparison.
    """
    
    world.ax.text(0.5, 0.5, message, transform=world.ax.transAxes,
                 fontsize=12, color='white', ha='center', va='center',
                 fontweight='bold', linespacing=1.5,
                 bbox=dict(facecolor='#2d2d2d', edgecolor='#4a90e2',
                          linewidth=2, boxstyle='round,pad=1'))
    
    plt.pause(1.5)  # Show completion page briefly before dashboard


# ==========================================
# Dashboard (clean, same as before)
# ==========================================
def show_dashboard(results):
    agents = [r["name"] for r in results]
    steps = [r["steps"] for r in results]
    rescued = [r["rescued"] for r in results]
    efficiency = [round(r["rescued"]/r["steps"] * 100, 1) if r["steps"] else 0 for r in results]

    plt.style.use("dark_background")
    
    fig = plt.figure(figsize=(12, 8))
    fig.patch.set_facecolor("#1e1e1e")
    fig.suptitle('Rescue Agent Performance Analysis', fontsize=16, 
                 color='white', y=0.98, fontweight='bold')

    # Steps comparison
    ax1 = plt.subplot(2, 2, 1)
    colors = ['#ff6b6b', '#4ecdc4', '#45b7d1']
    bars = ax1.bar(agents, steps, color=colors, edgecolor='white', linewidth=1.5)
    ax1.set_title('Total Steps Taken', color='white', fontsize=11, fontweight='bold')
    ax1.set_ylabel('Steps', color='white')
    ax1.tick_params(colors='white')
    ax1.set_facecolor('#2d2d2d')
    for bar, step in zip(bars, steps):
        ax1.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 1,
                f'{step}', ha='center', va='bottom', color='white', fontweight='bold')

    # Patients rescued
    ax2 = plt.subplot(2, 2, 2)
    bars = ax2.bar(agents, rescued, color=colors, edgecolor='white', linewidth=1.5)
    ax2.set_title('Patients Rescued', color='white', fontsize=11, fontweight='bold')
    ax2.set_ylabel('Patients', color='white')
    ax2.set_ylim(0, 4.5)
    ax2.tick_params(colors='white')
    ax2.set_facecolor('#2d2d2d')
    for bar, resc in zip(bars, rescued):
        ax2.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.1,
                f'{int(resc)}/4', ha='center', va='bottom', color='white', fontweight='bold')

    # Efficiency percentage
    ax3 = plt.subplot(2, 2, 3)
    ax3.plot(agents, efficiency, marker='o', linewidth=2, markersize=8,
             color='#ffd700', markerfacecolor='white', markeredgewidth=2)
    ax3.fill_between(range(len(agents)), efficiency, alpha=0.3, color='#ffd700')
    for i, eff in enumerate(efficiency):
        ax3.annotate(f'{eff}%', (agents[i], eff), 
                    textcoords="offset points", xytext=(0, 10), 
                    ha='center', color='white', fontweight='bold')
    ax3.set_title('Efficiency (Rescues per Step)', color='white', fontsize=11, fontweight='bold')
    ax3.set_ylabel('Efficiency %', color='white')
    ax3.tick_params(colors='white')
    ax3.set_facecolor('#2d2d2d')
    ax3.grid(True, alpha=0.2)

    # Summary card
    ax4 = plt.subplot(2, 2, 4)
    ax4.axis('off')
    ax4.set_facecolor('#2d2d2d')
    
    best_agent = agents[rescued.index(max(rescued))]
    fastest_agent = agents[steps.index(min(steps))]
    most_efficient = agents[efficiency.index(max(efficiency))]
    
    summary = f"""
    PERFORMANCE SUMMARY
    
    🏆 Best Agent: {best_agent}
       Rescued: {max(rescued)}/4 patients
    
    ⚡ Fastest Agent: {fastest_agent}
       Steps taken: {min(steps)}
    
    📈 Most Efficient: {most_efficient}
       Efficiency: {max(efficiency)}%
    """
    
    ax4.text(0.1, 0.5, summary, transform=ax4.transAxes,
            fontsize=11, color='white', verticalalignment='center',
            fontweight='bold',
            bbox=dict(facecolor='#1e1e1e', edgecolor='#4a90e2', 
                     linewidth=2, boxstyle='round,pad=0.8'))

    plt.tight_layout()
    plt.show()


# ==========================================
# MAIN LOOP (with completion page)
# ==========================================
def run():
    plt.ion()

    base_world = GridWorld()
    layout = base_world.copy_layout()

    world = GridWorld()
    world.load_layout(layout)
    world.setup_plot()
    world.fig.canvas.mpl_connect('key_press_event', on_key)

    options = ["1. Simple Reflex", "2. Model-Based", "3. Goal-Based"]
    used = []
    results = []

    for _ in range(3):
        global _selected_option
        _selected_option = None

        draw_menu(world, "Select Rescue Agent", options, used)

        while _selected_option is None or _selected_option in used:
            plt.pause(0.1)

        choice = _selected_option
        used.append(choice)

        world.load_layout(layout)
        world.steps = 0
        world.rescued = 0

        if choice == 0:
            agent = SimpleReflexRescueAgent(world)
            world.agent_type = "Simple Reflex"
        elif choice == 1:
            agent = ModelBasedReflexRescueAgent(world)
            world.agent_type = "Model-Based"
        else:
            agent = GoalBasedRescueAgent(world)
            world.agent_type = "Goal-Based"

        world.draw_grid("Starting rescue mission...")

        for _ in range(50):
            agent.act()
            if world.rescued >= 4:
                break

        results.append({
            "name": world.agent_type,
            "steps": world.steps,
            "rescued": world.rescued
        })

    # NEW: Show completion page before dashboard
    show_completion_page(world)

    plt.ioff()
    plt.show()

    show_dashboard(results)


if __name__ == "__main__":
    run()