using System;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Threading;
using System.Windows.Forms;
using soapframework;

namespace _2017Launcher
{
	// Token: 0x02000003 RID: 3
	public partial class Form1 : Form
	{
		// Token: 0x06000007 RID: 7 RVA: 0x00002274 File Offset: 0x00000474
		public Form1()
		{
			this.InitializeComponent();
		}

		// Token: 0x06000008 RID: 8 RVA: 0x00002304 File Offset: 0x00000504
		public void InitTimer()
		{
			this.timer1 = new System.Windows.Forms.Timer();
			this.timer1.Tick += this.timer1_Tick;
			this.timer1.Interval = 3500;
			this.timer1.Start();
		}

		// Token: 0x06000009 RID: 9 RVA: 0x00002344 File Offset: 0x00000544
		private void timer1_Tick(object sender, EventArgs e)
		{
			if (this.headcolor == "Pastel brown")
			{
				this.pictureBox5.BackColor = this.pictureBox2.BackColor;
			}
			if (this.headcolor == "Brown")
			{
				this.pictureBox5.BackColor = this.pictureBox3.BackColor;
			}
			if (this.headcolor == "Medium red")
			{
				this.pictureBox5.BackColor = this.pictureBox4.BackColor;
			}
			if (this.headcolor == "Cyan")
			{
				this.pictureBox5.BackColor = this.pictureBox1.BackColor;
			}
			if (this.torsocolor == "Pastel brown")
			{
				this.pictureBox6.BackColor = this.pictureBox2.BackColor;
			}
			if (this.torsocolor == "Brown")
			{
				this.pictureBox6.BackColor = this.pictureBox3.BackColor;
			}
			if (this.torsocolor == "Medium red")
			{
				this.pictureBox6.BackColor = this.pictureBox4.BackColor;
			}
			if (this.torsocolor == "Cyan")
			{
				this.pictureBox6.BackColor = this.pictureBox1.BackColor;
			}
			if (this.leftarmcolor == "Pastel brown")
			{
				this.pictureBox7.BackColor = this.pictureBox2.BackColor;
			}
			if (this.leftarmcolor == "Brown")
			{
				this.pictureBox7.BackColor = this.pictureBox3.BackColor;
			}
			if (this.leftarmcolor == "Medium red")
			{
				this.pictureBox7.BackColor = this.pictureBox4.BackColor;
			}
			if (this.leftarmcolor == "Cyan")
			{
				this.pictureBox7.BackColor = this.pictureBox1.BackColor;
			}
			if (this.rightarmcolor == "Pastel brown")
			{
				this.pictureBox8.BackColor = this.pictureBox2.BackColor;
			}
			if (this.rightarmcolor == "Brown")
			{
				this.pictureBox8.BackColor = this.pictureBox3.BackColor;
			}
			if (this.rightarmcolor == "Medium red")
			{
				this.pictureBox8.BackColor = this.pictureBox4.BackColor;
			}
			if (this.rightarmcolor == "Cyan")
			{
				this.pictureBox8.BackColor = this.pictureBox1.BackColor;
			}
			if (this.leftlegcolor == "Pastel brown")
			{
				this.pictureBox9.BackColor = this.pictureBox2.BackColor;
			}
			if (this.leftlegcolor == "Brown")
			{
				this.pictureBox9.BackColor = this.pictureBox3.BackColor;
			}
			if (this.leftlegcolor == "Medium red")
			{
				this.pictureBox9.BackColor = this.pictureBox4.BackColor;
			}
			if (this.leftlegcolor == "Cyan")
			{
				this.pictureBox9.BackColor = this.pictureBox1.BackColor;
			}
			if (this.rightlegcolor == "Pastel brown")
			{
				this.pictureBox10.BackColor = this.pictureBox2.BackColor;
			}
			if (this.rightlegcolor == "Brown")
			{
				this.pictureBox10.BackColor = this.pictureBox3.BackColor;
			}
			if (this.rightlegcolor == "Medium red")
			{
				this.pictureBox10.BackColor = this.pictureBox4.BackColor;
			}
			if (this.rightlegcolor == "Cyan")
			{
				this.pictureBox10.BackColor = this.pictureBox1.BackColor;
			}
			if (!this.started2017)
			{
				string hostscr = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Clients/2017M/gameserver.txt");
				hostscr = hostscr.Replace("%port%", this.textBox4.Text);
				string port = "64989";
				string ip = "localhost";
				string baseurl = "roblox.com";
				string http = this.http;
				this.started2017 = true;
				new Thread(delegate()
				{
					this.jmmwantsitstable(ip, port, baseurl, http, hostscr);
				})
				{
					IsBackground = true
				}.Start();
			}
		}

		// Token: 0x0600000A RID: 10 RVA: 0x000027BA File Offset: 0x000009BA
		private static void CopyFilesRecursively(string sourcePath, string targetPath)
		{
		}

		// Token: 0x0600000B RID: 11 RVA: 0x000027BC File Offset: 0x000009BC
		private static void ExecuteCommand(string command)
		{
			Process.Start(new ProcessStartInfo("cmd.exe", "/c " + command)
			{
				CreateNoWindow = true,
				UseShellExecute = false,
				RedirectStandardError = true,
				RedirectStandardOutput = true
			}).Close();
		}

		// Token: 0x0600000C RID: 12 RVA: 0x000027FC File Offset: 0x000009FC
		private void Form1_Load(object sender, EventArgs e)
		{
			Random random = new Random();
			this.num = random.Next();
			this.listBox1.Items.Clear();
			string[] directories = Directory.GetDirectories(AppDomain.CurrentDomain.BaseDirectory + "\\Clients");
			for (int i = 0; i < directories.Length; i++)
			{
				this.listBox1.Items.Add(Path.GetFileName(directories[i]));
			}
			this.InitTimer();
		}

		// Token: 0x0600000D RID: 13 RVA: 0x00002872 File Offset: 0x00000A72
		private void textBox2_TextChanged(object sender, EventArgs e)
		{
		}

		// Token: 0x0600000E RID: 14 RVA: 0x00002874 File Offset: 0x00000A74
		private void jmmwantsitstablebutjson(string ip, string port, string baseurl, string text, string req)
		{
			try
			{
				SOAP.jsonExecute(baseurl, ip + ":" + port, text, req);
			}
			catch
			{
			}
		}

		// Token: 0x0600000F RID: 15 RVA: 0x000028AC File Offset: 0x00000AAC
		private void jmmwantsitstable(string ip, string port, string baseurl, string req, string scr)
		{
			try
			{
				SOAP.ExecuteScript(ip + ":" + port, "RanScript", scr, "Test", "", baseurl, req);
			}
			catch
			{
			}
		}

		// Token: 0x06000010 RID: 16 RVA: 0x000028F4 File Offset: 0x00000AF4
		public static void OpenClient(string rbxexe, string args, string mapname, bool customization = false)
		{
			new Process
			{
				StartInfo = 
				{
					FileName = rbxexe,
					WorkingDirectory = Path.GetDirectoryName(rbxexe),
					Arguments = args
				}
			}.Start();
		}

		// Token: 0x06000011 RID: 17 RVA: 0x0000292C File Offset: 0x00000B2C
		private void button1_Click(object sender, EventArgs e)
		{
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/HostPort.txt"
			}.FileName))
			{
				streamWriter.WriteLine(this.textBox4.Text);
			}
			string text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Fix.ini");
			if (this.currentclient == "2022M")
			{
				string text2 = "";
				DialogResult dialogResult = MessageBox.Show("Would you like to host without filtering? (Clicking no is insecure!)", "Roblox Launcher", MessageBoxButtons.YesNo);
				if (dialogResult == DialogResult.Yes)
				{
					text2 = "_G.FilteringEnabled=true";
				}
				else if (dialogResult == DialogResult.No)
				{
					text2 = "_G.FilteringEnabled=false";
				}
				string value = string.Concat(new string[]
				{
					"<roblox xmlns:xmime=",
					text,
					"http://www.w3.org/2005/05/xmlmime",
					text,
					" xmlns:xsi=",
					text,
					"http://www.w3.org/2001/XMLSchema-instance",
					text,
					" xsi:noNamespaceSchemaLocation=",
					text,
					"http://www.localhost//roblox.xsd",
					text,
					" version=",
					text,
					"4",
					text,
					">\r\n    <External>null</External>\r\n    <External>nil</External>\r\n    <Item class=",
					text,
					"Script",
					text,
					" referent=",
					text,
					"RBXA9BF459DE88842189FF810D1F9615061",
					text,
					">\r\n\t\t<Properties>\r\n\t\t\t<bool name =",
					text,
					"Disabled",
					text,
					">false</bool>\r\n            <Content name=",
					text,
					"LinkedSource",
					text,
					"><null></null></Content>\r\n\t\t\t<string name =",
					text,
					"Name",
					text,
					">Script</string>\r\n            <string name=",
					text,
					"ScriptGuid",
					text,
					">{1166F3A8-F70B-4DAF-B7C6-3C89D8BBC049}</string>\r\n\t\t\t<ProtectedString name=",
					text,
					"Source",
					text,
					"><![CDATA[",
					text2,
					"]]></ProtectedString>\r\n            <BinaryString name=",
					text,
					"Tags",
					text,
					"></BinaryString>\r\n\t\t</Properties>\r\n\t</Item>\r\n</roblox>"
				});
				using (StreamWriter streamWriter2 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "shared/content/server.rbxmx"
				}.FileName))
				{
					streamWriter2.WriteLine(value);
				}
				string text3 = "\"";
				string rbxexe = AppDomain.CurrentDomain.BaseDirectory + "Clients/2022M/RobloxStudioBeta.exe";
				string text4 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/place.rbxl";
				string mapname = "place.rbxl";
				string args = string.Concat(new string[]
				{
					text3,
					"\" -localPlaceFile ",
					text,
					text4,
					text,
					" -task StartServer -port ",
					this.textBox4.Text,
					text3
				});
				Form1.OpenClient(rbxexe, args, mapname, false);
				return;
			}
			if (this.currentclient == "2016L")
			{
				string text5 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Clients/2016L/test.txt");
				text5 = text5.Replace("%port%", this.textBox4.Text);
				using (StreamWriter streamWriter3 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "/Clients/2016L/gameserver.txt"
				}.FileName))
				{
					streamWriter3.WriteLine(text5);
				}
				Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "Clients/" + this.currentclient + "/start.bat")
				{
					UseShellExecute = true,
					WindowStyle = ProcessWindowStyle.Minimized
				});
				return;
			}
			if (this.currentclient == "2017M")
			{
				Form1.ExecuteCommand("start Clients/" + this.currentclient + "/Player/RccService.exe -Console -verbose -placeid:1818 -port 64989");
				this.started2017 = false;
				return;
			}
			string text6 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/gameserverraw.json");
			text6 = text6.Replace("%port%", this.textBox4.Text);
			using (StreamWriter streamWriter4 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "gameserver.json"
			}.FileName))
			{
				streamWriter4.WriteLine(text6);
			}
			Form1.ExecuteCommand(string.Concat(new string[]
			{
				"start shared/",
				this.currentclient,
				".exe -Console -verbose -placeid:1818 -localtest ",
				text,
				"gameserver.json",
				text,
				"  -port 64989"
			}));
		}

		// Token: 0x06000012 RID: 18 RVA: 0x00002DF8 File Offset: 0x00000FF8
		private void button2_Click(object sender, EventArgs e)
		{
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/username.txt"
			}.FileName))
			{
				streamWriter.WriteLine(this.textBox1.Text);
			}
			using (StreamWriter streamWriter2 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/ip.txt"
			}.FileName))
			{
				streamWriter2.WriteLine(this.textBox3.Text);
			}
			using (StreamWriter streamWriter3 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/clientport.txt"
			}.FileName))
			{
				streamWriter3.WriteLine(this.textBox2.Text);
			}
			string text = "_G.ShowNames=true";
			string text2 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Fix.ini");
			string text3 = string.Concat(new string[]
			{
				File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini"),
				";password=",
				this.num.ToString(),
				"|",
				this.headcolor,
				";",
				this.torsocolor,
				";",
				this.leftarmcolor,
				";",
				this.rightarmcolor,
				";",
				this.leftlegcolor,
				";",
				this.rightlegcolor
			});
			string mapname = "1818";
			string rbxexe = AppDomain.CurrentDomain.BaseDirectory + "Clients/2022M/RobloxStudioBeta.exe";
			string text4 = "\"";
			if (this.currentclient == "2022M")
			{
				text3 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini");
				string text5 = string.Concat(new string[]
				{
					text,
					" _G.app='",
					text3,
					"' print(_G.app)\r\norigstring =_G.app\r\nlocal foundchar=false\r\nlocal username1 = '",
					this.textBox1.Text.Replace("\n", "").Replace("\r", ""),
					"'  \r\nlocal username = '",
					this.textBox1.Text.Replace("\n", "").Replace("\r", ""),
					"' \r\nlocal a=Instance.new('StringValue') a.Parent=game:GetService('ReplicatedStorage') a.Name=game:GetService('Players').LocalPlayer.Name a.Value=username\r\nlocal number= nil\r\n local words = {}\r\nfor w in (origstring .. ';'):gmatch('([^;]*);') do \r\n    table.insert(words, w) \r\nend\r\nlocal num1=words[1]\r\nfunction loadchar()\r\nwait(1)\r\nlocal char = game:GetService('Players').LocalPlayer.Character\r\nfor i,v in pairs(words) do\r\n    pcall(function()\r\n\tlocal a=game:GetService('ReplicatedStorage'):FindFirstChild('charapp')\r\n     a:FireServer(v)\r\n\t end)\r\n\tend\r\ngame:GetService('ReplicatedStorage').BodyColorsRemote:FireServer('",
					this.headcolor,
					";",
					this.torsocolor,
					";",
					this.leftarmcolor,
					";",
					this.rightarmcolor,
					";",
					this.leftlegcolor,
					";",
					this.rightlegcolor,
					"')\r\nlocal a={}\r\ngame:GetService('ReplicatedStorage').Nametag:FireServer(username)\r\nend\r\ngame:GetService('Players').PlayerAdded:connect(function(plr)\r\nif plr == game:GetService('Players').LocalPlayer then\r\nfoundchar=true\r\nif workspace:FindFirstChild(plr.Name) then\r\nif plr.Character~=nil then\r\nloadchar()\r\nend\r\nend\r\ngame:GetService('Players').LocalPlayer.CharacterAdded:connect(function()\r\npcall(function()\r\nloadchar()\r\nend)\r\nend)\r\nend\r\nend)\r\nrepeat wait() until game:GetService('Players').LocalPlayer.Character~=nil\r\nlocal char=game:GetService('Players').LocalPlayer.Character\r\n\r\nwait(0.1)\r\nif foundchar==false and game:GetService('Players').LocalPlayer~=nil then\r\nloadchar()\r\ngame:GetService('Players').LocalPlayer.CharacterAdded:connect(function()\r\npcall(function()\r\nloadchar()\r\nend)\r\nend)\r\nelse\r\nrepeat wait() until game:GetService('Players').LocalPlayer~=nil\r\nloadchar()\r\ngame:GetService('Players').LocalPlayer.CharacterAdded:connect(function()\r\npcall(function()\r\nloadchar()\r\nend)\r\nend)\r\nend\r\nlocal shortcut=Instance.new('BoolValue',game:GetService('Players').LocalPlayer) shortcut.Name='ShowNames' shortcut.Value=_G.ShowNames"
				});
				string value = string.Concat(new string[]
				{
					"<roblox xmlns:xmime=",
					text2,
					"http://www.w3.org/2005/05/xmlmime",
					text2,
					" xmlns:xsi=",
					text2,
					"http://www.w3.org/2001/XMLSchema-instance",
					text2,
					" xsi:noNamespaceSchemaLocation=",
					text2,
					"http://www.localhost//roblox.xsd",
					text2,
					" version=",
					text2,
					"4",
					text2,
					">\r\n    <External>null</External>\r\n    <External>nil</External>\r\n    <Item class=",
					text2,
					"LocalScript",
					text2,
					" referent=",
					text2,
					"RBXA9BF459DE88842189FF810D1F9615061",
					text2,
					">\r\n\t\t<Properties>\r\n\t\t\t<bool name =",
					text2,
					"Disabled",
					text2,
					">false</bool>\r\n            <Content name=",
					text2,
					"LinkedSource",
					text2,
					"><null></null></Content>\r\n\t\t\t<string name =",
					text2,
					"Name",
					text2,
					">LocalScript</string>\r\n            <string name=",
					text2,
					"ScriptGuid",
					text2,
					">{1166F3A8-F70B-4DAF-B7C6-3C89D8BBC049}</string>\r\n\t\t\t<ProtectedString name=",
					text2,
					"Source",
					text2,
					"><![CDATA[",
					text5,
					"]]></ProtectedString>\r\n            <BinaryString name=",
					text2,
					"Tags",
					text2,
					"></BinaryString>\r\n\t\t</Properties>\r\n\t</Item>\r\n</roblox>"
				});
				using (StreamWriter streamWriter4 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "shared/content/test.rbxmx"
				}.FileName))
				{
					streamWriter4.WriteLine(value);
				}
				string args = string.Concat(new string[]
				{
					text4,
					"\"-task StartClient -server ",
					text2,
					this.textBox3.Text.Replace("\n", "").Replace("\r", ""),
					text2,
					" -port ",
					this.textBox2.Text,
					text4
				});
				Form1.OpenClient(rbxexe, args, mapname, false);
				return;
			}
			if (this.currentclient == "2016L")
			{
				Form1.ExecuteCommand(string.Concat(new string[]
				{
					"start Clients/",
					this.currentclient,
					"/Player/RobloxPlayerBeta.exe -a ",
					text2,
					"https://localhost/login/negotiate.ashx",
					text2,
					" -j ",
					text2,
					"https://localhost/game/join.php/?placeid=1818&ip=",
					this.textBox3.Text,
					"&port=",
					this.textBox2.Text,
					"&id=",
					this.num.ToString(),
					"&app=",
					text3,
					"&user=",
					this.textBox1.Text,
					text2,
					" -t ",
					text2,
					"1",
					text2
				}));
				return;
			}
			if (this.currentclient == "2017M")
			{
				Form1.ExecuteCommand(string.Concat(new string[]
				{
					"start Clients/",
					this.currentclient,
					"/Player/RobloxPlayerBeta.exe -a ",
					text2,
					"https://localhost/login/negotiate.ashx",
					text2,
					" -j ",
					text2,
					"https://localhost/game/join.php/?placeid=1818&ip=",
					this.textBox3.Text,
					"&port=",
					this.textBox2.Text,
					"&id=",
					this.num.ToString(),
					"&app=",
					text3,
					"&user=",
					this.textBox1.Text,
					text2,
					" -t ",
					text2,
					"1",
					text2
				}));
				return;
			}
			Form1.ExecuteCommand(string.Concat(new string[]
			{
				"start Clients/",
				this.currentclient,
				"/Player/RobloxPlayerBeta.exe -a ",
				text2,
				"https://localhost/login/negotiate.ashx",
				text2,
				" -j ",
				text2,
				"https://localhost/game/placelauncher.ashx?&year=2018&placeid=1818&ip=",
				this.textBox3.Text,
				"&port=",
				this.textBox2.Text,
				"&id=",
				this.num.ToString(),
				"&app=",
				text3,
				"&user=",
				this.textBox1.Text,
				text2,
				" -t ",
				text2,
				"1",
				text2
			}));
		}

		// Token: 0x06000013 RID: 19 RVA: 0x00003604 File Offset: 0x00001804
		private void Form1_Shown(object sender, EventArgs e)
		{
			Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "WebServer/Start.bat")
			{
				UseShellExecute = true,
				WindowStyle = ProcessWindowStyle.Minimized
			});
			string text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/username.txt");
			text = text.Remove(text.Length - 1, 1);
			this.textBox1.Text = text;
			text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/ip.txt");
			text = text.Remove(text.Length - 1, 1);
			this.textBox3.Text = text;
			text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/clientport.txt");
			text = text.Remove(text.Length - 1, 1);
			this.textBox2.Text = text;
			text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/HostPort.txt");
			text = text.Remove(text.Length - 1, 1);
			this.textBox4.Text = text;
			text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/SelectedClient.txt");
			this.listBox1.SetSelected(this.listBox1.FindString(text), true);
			text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/HeadColor.txt");
			this.headcolor = text;
			text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/TorsoColor.txt");
			this.torsocolor = text;
			text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/LeftArmColor.txt");
			this.leftarmcolor = text;
			text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/RightArmColor.txt");
			this.rightarmcolor = text;
			text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/LeftLegColor.txt");
			this.leftlegcolor = text;
			text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/RightLegColor.txt");
			this.rightlegcolor = text;
		}

		// Token: 0x06000014 RID: 20 RVA: 0x00003810 File Offset: 0x00001A10
		private void button3_Click(object sender, EventArgs e)
		{
			OpenFileDialog openFileDialog = new OpenFileDialog();
			openFileDialog.InitialDirectory = "c:\\";
			openFileDialog.Filter = "Roblox files (*.rbxl)|*.rbxl";
			openFileDialog.FilterIndex = 0;
			openFileDialog.RestoreDirectory = true;
			if (openFileDialog.ShowDialog() == DialogResult.OK)
			{
				string fileName = openFileDialog.FileName;
				string path = AppDomain.CurrentDomain.BaseDirectory + "Webserver/www/.127.0.0.1/asset/1818";
				if (File.Exists(path))
				{
					File.Delete(path);
				}
				string destFileName = AppDomain.CurrentDomain.BaseDirectory + "Webserver/www/.127.0.0.1/asset/1818";
				try
				{
					File.Copy(fileName, destFileName, true);
				}
				catch (IOException ex)
				{
					Console.WriteLine(ex.Message);
				}
				string fileName2 = openFileDialog.FileName;
				string path2 = AppDomain.CurrentDomain.BaseDirectory + "Clients/2016L/Player/content/1818";
				if (File.Exists(path2))
				{
					File.Delete(path2);
				}
				string destFileName2 = AppDomain.CurrentDomain.BaseDirectory + "Clients/2016L/Player/content/1818";
				try
				{
					File.Copy(fileName2, destFileName2, true);
				}
				catch (IOException ex2)
				{
					Console.WriteLine(ex2.Message);
				}
				string fileName3 = openFileDialog.FileName;
				string path3 = AppDomain.CurrentDomain.BaseDirectory + "Clients/2017M/Player/content/1818";
				if (File.Exists(path3))
				{
					File.Delete(path3);
				}
				string destFileName3 = AppDomain.CurrentDomain.BaseDirectory + "Clients/2017M/Player/content/1818";
				try
				{
					File.Copy(fileName3, destFileName3, true);
				}
				catch (IOException ex3)
				{
					Console.WriteLine(ex3.Message);
				}
				string fileName4 = openFileDialog.FileName;
				string path4 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/place.rbxl";
				if (File.Exists(path4))
				{
					File.Delete(path4);
				}
				string destFileName4 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/place.rbxl";
				try
				{
					File.Copy(fileName4, destFileName4, true);
				}
				catch (IOException ex4)
				{
					Console.WriteLine(ex4.Message);
				}
			}
		}

		// Token: 0x06000015 RID: 21 RVA: 0x000039F0 File Offset: 0x00001BF0
		private void Form1_FormClosing(object sender, FormClosingEventArgs e)
		{
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/SelectedClient.txt"
			}.FileName))
			{
				streamWriter.Write(this.currentclient);
			}
			using (StreamWriter streamWriter2 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/HeadColor.txt"
			}.FileName))
			{
				streamWriter2.Write(this.headcolor);
			}
			using (StreamWriter streamWriter3 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/TorsoColor.txt"
			}.FileName))
			{
				streamWriter3.Write(this.torsocolor);
			}
			using (StreamWriter streamWriter4 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/LeftArmColor.txt"
			}.FileName))
			{
				streamWriter4.Write(this.leftarmcolor);
			}
			using (StreamWriter streamWriter5 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/RightArmColor.txt"
			}.FileName))
			{
				streamWriter5.Write(this.rightarmcolor);
			}
			using (StreamWriter streamWriter6 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/LeftLegColor.txt"
			}.FileName))
			{
				streamWriter6.Write(this.leftlegcolor);
			}
			using (StreamWriter streamWriter7 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/RightLegColor.txt"
			}.FileName))
			{
				streamWriter7.Write(this.rightlegcolor);
			}
			Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "WebServer/kill.bat")
			{
				UseShellExecute = true,
				WindowStyle = ProcessWindowStyle.Minimized
			});
		}

		// Token: 0x06000016 RID: 22 RVA: 0x00003C5C File Offset: 0x00001E5C
		private void textBox1_TextChanged(object sender, EventArgs e)
		{
		}

		// Token: 0x06000017 RID: 23 RVA: 0x00003C5E File Offset: 0x00001E5E
		private void textBox4_TextChanged(object sender, EventArgs e)
		{
		}

		// Token: 0x06000018 RID: 24 RVA: 0x00003C60 File Offset: 0x00001E60
		private void Form1_FormClosed(object sender, FormClosedEventArgs e)
		{
		}

		// Token: 0x06000019 RID: 25 RVA: 0x00003C64 File Offset: 0x00001E64
		private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
		{
			string str = "password=" + this.num.ToString();
			string str2 = "_G.AdminPasswordPublic = '" + str + "'\r\n\r\n";
			string text = this.listBox1.SelectedItem.ToString();
			if (text == "2022M")
			{
				Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "/Hosts/Play.bat")
				{
					UseShellExecute = true,
					WindowStyle = ProcessWindowStyle.Minimized
				});
				this.currentclient = text;
				return;
			}
			if (text == "2017M")
			{
				this.currentclient = text;
				return;
			}
			try
			{
				string str3 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings\\ServerScript.txt");
				string path = AppDomain.CurrentDomain.BaseDirectory.ToString() + "Clients\\" + text + "\\Player\\content\\scripts\\CoreScripts\\ServerStarterScript.lua";
				this.currentclient = text;
				File.WriteAllText(path, str2 + str3);
			}
			catch
			{
				string str4 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings\\ServerScript.txt");
				string path2 = AppDomain.CurrentDomain.BaseDirectory.ToString() + "shared\\content\\scripts\\CoreScripts\\ServerStarterScript.lua";
				this.currentclient = text;
				File.WriteAllText(path2, str2 + str4);
			}
		}

		// Token: 0x0600001A RID: 26 RVA: 0x00003DAC File Offset: 0x00001FAC
		private void checkedListBox1_SelectedIndexChanged(object sender, EventArgs e)
		{
		}

		// Token: 0x0600001B RID: 27 RVA: 0x00003DB0 File Offset: 0x00001FB0
		private void pictureBox1_Click(object sender, EventArgs e)
		{
			if (this.selectedbodypart == "Head")
			{
				this.headcolor = "Cyan";
				this.pictureBox5.BackColor = this.pictureBox1.BackColor;
			}
			if (this.selectedbodypart == "Torso")
			{
				this.torsocolor = "Cyan";
				this.pictureBox6.BackColor = this.pictureBox1.BackColor;
			}
			if (this.selectedbodypart == "Left Arm")
			{
				this.leftarmcolor = "Cyan";
				this.pictureBox7.BackColor = this.pictureBox1.BackColor;
			}
			if (this.selectedbodypart == "Right Arm")
			{
				this.rightarmcolor = "Cyan";
				this.pictureBox8.BackColor = this.pictureBox1.BackColor;
			}
			if (this.selectedbodypart == "Left Leg")
			{
				this.leftlegcolor = "Cyan";
				this.pictureBox9.BackColor = this.pictureBox1.BackColor;
			}
			if (this.selectedbodypart == "Right Leg")
			{
				this.rightlegcolor = "Cyan";
				this.pictureBox10.BackColor = this.pictureBox1.BackColor;
			}
		}

		// Token: 0x0600001C RID: 28 RVA: 0x00003EF0 File Offset: 0x000020F0
		private void pictureBox2_Click(object sender, EventArgs e)
		{
			if (this.selectedbodypart == "Head")
			{
				this.headcolor = "Pastel brown";
				this.pictureBox5.BackColor = this.pictureBox2.BackColor;
			}
			if (this.selectedbodypart == "Torso")
			{
				this.torsocolor = "Pastel brown";
				this.pictureBox6.BackColor = this.pictureBox2.BackColor;
			}
			if (this.selectedbodypart == "Left Arm")
			{
				this.leftarmcolor = "Pastel brown";
				this.pictureBox7.BackColor = this.pictureBox2.BackColor;
			}
			if (this.selectedbodypart == "Right Arm")
			{
				this.rightarmcolor = "Pastel brown";
				this.pictureBox8.BackColor = this.pictureBox2.BackColor;
			}
			if (this.selectedbodypart == "Left Leg")
			{
				this.leftlegcolor = "Pastel brown";
				this.pictureBox9.BackColor = this.pictureBox2.BackColor;
			}
			if (this.selectedbodypart == "Right Leg")
			{
				this.rightlegcolor = "Pastel brown";
				this.pictureBox10.BackColor = this.pictureBox2.BackColor;
			}
		}

		// Token: 0x0600001D RID: 29 RVA: 0x00004030 File Offset: 0x00002230
		private void pictureBox3_Click(object sender, EventArgs e)
		{
			if (this.selectedbodypart == "Head")
			{
				this.headcolor = "Brown";
				this.pictureBox5.BackColor = this.pictureBox3.BackColor;
			}
			if (this.selectedbodypart == "Torso")
			{
				this.torsocolor = "Brown";
				this.pictureBox6.BackColor = this.pictureBox3.BackColor;
			}
			if (this.selectedbodypart == "Left Arm")
			{
				this.leftarmcolor = "Brown";
				this.pictureBox7.BackColor = this.pictureBox3.BackColor;
			}
			if (this.selectedbodypart == "Right Arm")
			{
				this.rightarmcolor = "Brown";
				this.pictureBox8.BackColor = this.pictureBox3.BackColor;
			}
			if (this.selectedbodypart == "Left Leg")
			{
				this.leftlegcolor = "Brown";
				this.pictureBox9.BackColor = this.pictureBox3.BackColor;
			}
			if (this.selectedbodypart == "Right Leg")
			{
				this.rightlegcolor = "Brown";
				this.pictureBox10.BackColor = this.pictureBox3.BackColor;
			}
		}

		// Token: 0x0600001E RID: 30 RVA: 0x00004170 File Offset: 0x00002370
		private void pictureBox4_Click(object sender, EventArgs e)
		{
			if (this.selectedbodypart == "Head")
			{
				this.headcolor = "Medium red";
				this.pictureBox5.BackColor = this.pictureBox4.BackColor;
			}
			if (this.selectedbodypart == "Torso")
			{
				this.torsocolor = "Medium red";
				this.pictureBox6.BackColor = this.pictureBox4.BackColor;
			}
			if (this.selectedbodypart == "Left Arm")
			{
				this.leftarmcolor = "Medium red";
				this.pictureBox7.BackColor = this.pictureBox4.BackColor;
			}
			if (this.selectedbodypart == "Right Arm")
			{
				this.rightarmcolor = "Medium red";
				this.pictureBox8.BackColor = this.pictureBox4.BackColor;
			}
			if (this.selectedbodypart == "Left Leg")
			{
				this.leftlegcolor = "Medium red";
				this.pictureBox9.BackColor = this.pictureBox4.BackColor;
			}
			if (this.selectedbodypart == "Right Leg")
			{
				this.rightlegcolor = "Medium red";
				this.pictureBox10.BackColor = this.pictureBox4.BackColor;
			}
		}

		// Token: 0x0600001F RID: 31 RVA: 0x000042AF File Offset: 0x000024AF
		private void button4_Click(object sender, EventArgs e)
		{
			Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "WebServer/Start.bat")
			{
				UseShellExecute = true,
				WindowStyle = ProcessWindowStyle.Minimized
			});
		}

		// Token: 0x06000020 RID: 32 RVA: 0x000042DE File Offset: 0x000024DE
		private void button5_Click(object sender, EventArgs e)
		{
			Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "WebServer/kill.bat")
			{
				UseShellExecute = true,
				WindowStyle = ProcessWindowStyle.Minimized
			});
		}

		// Token: 0x06000021 RID: 33 RVA: 0x0000430D File Offset: 0x0000250D
		private void pictureBox5_Click(object sender, EventArgs e)
		{
			this.selectedbodypart = "Head";
		}

		// Token: 0x06000022 RID: 34 RVA: 0x0000431A File Offset: 0x0000251A
		private void pictureBox6_Click(object sender, EventArgs e)
		{
			this.selectedbodypart = "Torso";
		}

		// Token: 0x06000023 RID: 35 RVA: 0x00004327 File Offset: 0x00002527
		private void pictureBox7_Click(object sender, EventArgs e)
		{
			this.selectedbodypart = "Left Arm";
		}

		// Token: 0x06000024 RID: 36 RVA: 0x00004334 File Offset: 0x00002534
		private void pictureBox8_Click(object sender, EventArgs e)
		{
			this.selectedbodypart = "Right Arm";
		}

		// Token: 0x06000025 RID: 37 RVA: 0x00004341 File Offset: 0x00002541
		private void pictureBox9_Click(object sender, EventArgs e)
		{
			this.selectedbodypart = "Left Leg";
		}

		// Token: 0x06000026 RID: 38 RVA: 0x0000434E File Offset: 0x0000254E
		private void pictureBox10_Click(object sender, EventArgs e)
		{
			this.selectedbodypart = "Right Leg";
		}

		// Token: 0x04000001 RID: 1
		private string http = "http";

		// Token: 0x04000002 RID: 2
		private int num;

		// Token: 0x04000003 RID: 3
		private string headcolor = "Pastel brown";

		// Token: 0x04000004 RID: 4
		private string torsocolor = "Pastel brown";

		// Token: 0x04000005 RID: 5
		private string leftlegcolor = "Pastel brown";

		// Token: 0x04000006 RID: 6
		private string rightlegcolor = "Pastel brown";

		// Token: 0x04000007 RID: 7
		private string leftarmcolor = "Pastel brown";

		// Token: 0x04000008 RID: 8
		private string rightarmcolor = "Pastel brown";

		// Token: 0x04000009 RID: 9
		private bool started2017 = true;

		// Token: 0x0400000A RID: 10
		private Point startPoint = new Point(0, 0);

		// Token: 0x0400000B RID: 11
		private System.Windows.Forms.Timer timer1;

		// Token: 0x0400000C RID: 12
		private string selectedbodypart = "Head";

		// Token: 0x0400000D RID: 13
		private string currentclient = "2018M";
	}
}
