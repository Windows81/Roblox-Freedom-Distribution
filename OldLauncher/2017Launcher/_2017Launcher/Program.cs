using System;
using System.Windows.Forms;

namespace _2017Launcher
{
	// Token: 0x0200000F RID: 15
	internal static class Program
	{
		// Token: 0x06000086 RID: 134 RVA: 0x0000D228 File Offset: 0x0000B428
		[STAThread]
		private static void Main()
		{
			Application.EnableVisualStyles();
			Application.SetCompatibleTextRenderingDefault(false);
			Application.Run(new Form1());
		}
	}
}
