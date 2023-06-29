using System;
using System.Windows.Forms;

namespace _2017Launcher
{
	// Token: 0x02000004 RID: 4
	internal static class Program
	{
		// Token: 0x06000029 RID: 41 RVA: 0x0000594C File Offset: 0x00003B4C
		[STAThread]
		private static void Main()
		{
			Application.EnableVisualStyles();
			Application.SetCompatibleTextRenderingDefault(false);
			Application.Run(new Form1());
		}
	}
}
