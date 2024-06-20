import threading
import time
import VisPosAuto as Vis

# Global instance
vis_instance = Vis.VisualPositionAuto(5, 5, Vis.screen_size)

def run_pygame():
    vis_instance.run()

def main():
    pygame_thread = threading.Thread(target=run_pygame)
    pygame_thread.start()

    # Example usage: Change the color of squares in order
    while True:
        for i in range(25):
            vis_instance.change_all_square_colors(Vis.GREY)
            vis_instance.change_square_color(i, Vis.RED)
            time.sleep(0.2)

if __name__ == '__main__':
    main()
