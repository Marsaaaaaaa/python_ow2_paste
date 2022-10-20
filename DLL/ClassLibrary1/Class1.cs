using InputInterceptorNS;
using System;
using System.Runtime.InteropServices;
using System.Linq;
using System.Threading;

namespace ClassLibrary1
{
    public class Class1
    {
        public void click_mouse()
        {
            MouseHook mouseHook = new MouseHook();
            mouseHook.SimulateLeftButtonClick(50);
        }
        public void only_move_mouse(int x, int y)
        {
            MouseHook mouseHook = new MouseHook();
            mouseHook.MoveCursorBy(x, y, false);
        }

        public void rclick_mouse()
        {
            MouseHook mouseHook = new MouseHook();
            mouseHook.SimulateRightButtonClick(50);
        }
        public void simulate_shift()
        {      
            KeyboardHook KbHook = new KeyboardHook();
            KbHook.SimulateKeyPress(KeyCode.LeftShift, 50);

        }
        public void simulate_Q()
        {
            KeyboardHook KbHook = new KeyboardHook();
            KbHook.SimulateKeyPress(KeyCode.Q, 50);

        }

        public void simulate_E()
        {
            KeyboardHook KbHook = new KeyboardHook();
            KbHook.SimulateKeyPress(KeyCode.E, 50);
        }


        public void move_mouse(float x, float y, int box_size, float x_multiplier, float y_multiplier, float y_diff)
        {
            /*float xr;
            if (x > box_size)
            {
                xr = -(960 - x);
                if ((xr + 960) > 1920)
                {
                    xr = 0;
                }
            }
            else
            {
                xr = x;
            }*/
            float yr;
            if (y > box_size)
            {
                yr = -(540 - y);
                if ((yr + 540) > 1080)
                {
                    yr = 0;
                }
            }
            else
            {
                yr = y;
            }
            int yf = (int)((yr - y_diff) * y_multiplier);

            float speedMultiplier = (algo_speed - 10) / (10);
            short xf;
            if (x > box_size)
            {
                xf = (short)(x / ((x * (-1 * speedMultiplier) + 100) / 200) / (2 + 3.3 / x_multiplier));
            }
            else
            {
                xf = (short)((x * -1) / ((((x * - 1) *(speedMultiplier) + 100) * -1)/200 / 2 + 3.3/ x_multiplier));
            }
            only_move_mouse(xf, yf);
            Thread.Sleep(5);
            // click_mouse();

        }
        [DllImport("user32.dll")]
        static extern short GetAsyncKeyState(int VirtualKeyPressed);
        public static bool is_activated(int key)
        {
            if (GetAsyncKeyState(key) == 0)
                return false;
            else
                return true;
        }
        public bool Check(float a, int b)
        {
            if (a > b)
            {
                return true;
            }
            else
            {
                return false;
            }
        }
        public void Run_Me()
        {
            InputInterceptor.Initialize();
        }
    }
}
