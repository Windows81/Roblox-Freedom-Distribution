using System;
using System.CodeDom.Compiler;
using System.Configuration;
using System.Runtime.CompilerServices;

namespace _2017Launcher.Properties
{
	// Token: 0x02000011 RID: 17
	[CompilerGenerated]
	[GeneratedCode("Microsoft.VisualStudio.Editors.SettingsDesigner.SettingsSingleFileGenerator", "16.10.0.0")]
	internal sealed partial class Settings : ApplicationSettingsBase
	{
		// Token: 0x17000013 RID: 19
		// (get) Token: 0x06000098 RID: 152 RVA: 0x0000D3E1 File Offset: 0x0000B5E1
		public static Settings Default
		{
			get
			{
				return Settings.defaultInstance;
			}
		}

		// Token: 0x04000084 RID: 132
		private static Settings defaultInstance = (Settings)SettingsBase.Synchronized(new Settings());
	}
}
