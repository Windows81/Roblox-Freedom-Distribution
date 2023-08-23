using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Linq.Expressions;
using System.Net;
using System.Runtime.CompilerServices;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading;
using System.Windows.Forms;
using System.Xml.Linq;
using GameServer;
using GameServer.Rcc;
using GameServer.Rcc.Classes;
using Microsoft.CSharp.RuntimeBinder;
using soapframework;
using SoapUI.Rcc.Classes;
using _2017Launcher.Properties;

namespace _2017Launcher
{
	// Token: 0x0200000E RID: 14
	public partial class Form1 : Form
	{
		// Token: 0x06000035 RID: 53 RVA: 0x00003BAC File Offset: 0x00001DAC
		public Form1()
		{
			this.InitializeComponent();
		}

		// Token: 0x06000036 RID: 54 RVA: 0x00003C66 File Offset: 0x00001E66
		public string Get_Form1Text()
		{
			return this.textBox2.Text;
		}

		// Token: 0x06000037 RID: 55 RVA: 0x00003C73 File Offset: 0x00001E73
		public void InitTimer()
		{
			this.timer1 = new System.Windows.Forms.Timer();
			this.timer1.Tick += this.timer1_Tick;
			this.timer1.Interval = 3500;
			this.timer1.Start();
		}

		// Token: 0x06000038 RID: 56 RVA: 0x00003CB4 File Offset: 0x00001EB4
		private void timer1_Tick(object sender, EventArgs e)
		{
			if (this.label5.Text != "Clothing")
			{
				this.label5.Text = "Clothing";
			}
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
				string hostscr = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/shared/2017host.txt");
				hostscr = hostscr.Replace("%bodytype%", this.chartype);
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
			if (!this.started2008)
			{
				string script = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/shared/2008host.txt");
				string s = "64989";
				string ip2 = "localhost";
				string url = "localhost/";
				string text = this.http;
				this.started2008 = true;
				Form1.<timer1_Tick>g__ParseXML|18_1(SOAP2.OpenJob(int.Parse(s), new Job("Test", double.Parse("600000"), 0, double.Parse("0")), new Script("GameServer", script, this.<timer1_Tick>g__GetLuaValues|18_2()), url, ip2), "OpenJob");
			}
		}

		// Token: 0x06000039 RID: 57 RVA: 0x000041F4 File Offset: 0x000023F4
		public static void CopyFilesRecursively(DirectoryInfo source, DirectoryInfo target)
		{
			foreach (DirectoryInfo directoryInfo in source.GetDirectories())
			{
				try
				{
					Form1.CopyFilesRecursively(directoryInfo, target.CreateSubdirectory(directoryInfo.Name));
				}
				catch (Exception)
				{
				}
			}
			foreach (FileInfo fileInfo in source.GetFiles())
			{
				if (File.Exists(target.FullName + "\\" + fileInfo.Name))
				{
					File.Delete(target.FullName + "\\" + fileInfo.Name);
				}
				fileInfo.CopyTo(Path.Combine(target.FullName, fileInfo.Name));
			}
		}

		// Token: 0x0600003A RID: 58 RVA: 0x000042B0 File Offset: 0x000024B0
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

		// Token: 0x0600003B RID: 59 RVA: 0x000042F0 File Offset: 0x000024F0
		private void Form1_Load(object sender, EventArgs e)
		{
			if (!Directory.Exists(AppDomain.CurrentDomain.BaseDirectory + "\\Clients"))
			{
				Directory.CreateDirectory(AppDomain.CurrentDomain.BaseDirectory + "\\Clients");
			}
			if (!Directory.Exists(AppDomain.CurrentDomain.BaseDirectory + "\\Settings"))
			{
				Directory.CreateDirectory(AppDomain.CurrentDomain.BaseDirectory + "\\Settings");
			}
			if (!Directory.Exists(AppDomain.CurrentDomain.BaseDirectory + "\\Settings\\assetsaving"))
			{
				Directory.CreateDirectory(AppDomain.CurrentDomain.BaseDirectory + "\\Settings\\assetsaving");
			}
			if (!Directory.Exists(AppDomain.CurrentDomain.BaseDirectory + "\\Settings\\BodyColors"))
			{
				Directory.CreateDirectory(AppDomain.CurrentDomain.BaseDirectory + "\\Settings\\BodyColors");
			}
			this.listBox1.Items.Clear();
			string[] directories = Directory.GetDirectories(AppDomain.CurrentDomain.BaseDirectory + "\\Clients");
			for (int i = 0; i < directories.Length; i++)
			{
				this.listBox1.Items.Add(Path.GetFileName(directories[i]));
			}
			this.InitTimer();
		}

		// Token: 0x0600003C RID: 60 RVA: 0x00004428 File Offset: 0x00002628
		private void textBox2_TextChanged(object sender, EventArgs e)
		{
		}

		// Token: 0x0600003D RID: 61 RVA: 0x0000442C File Offset: 0x0000262C
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

		// Token: 0x0600003E RID: 62 RVA: 0x00004464 File Offset: 0x00002664
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

		// Token: 0x0600003F RID: 63 RVA: 0x000044AC File Offset: 0x000026AC
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

		// Token: 0x06000040 RID: 64 RVA: 0x000044E4 File Offset: 0x000026E4
		private void button1_Click(object sender, EventArgs e)
		{
			string text = this.listBox1.SelectedItem.ToString();
			if (text == "Empty")
			{
				return;
			}
			string str = "password=" + this.num.ToString();
			string str2 = "_G.AdminPasswordPublic = '" + str + "'\r\n\r\n";
			try
			{
				string text2 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings\\ServerScript.txt");
				string path = AppDomain.CurrentDomain.BaseDirectory.ToString() + "Clients\\" + text + "\\Player\\content\\scripts\\CoreScripts\\ServerStarterScript.lua";
				text2 = text2.Replace("%bodytype%", this.chartype);
				File.WriteAllText(path, str2 + text2);
			}
			catch
			{
				string text3 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings\\ServerScript.txt");
				string path2 = AppDomain.CurrentDomain.BaseDirectory.ToString() + "shared\\content\\scripts\\CoreScripts\\ServerStarterScript.lua";
				text3 = text3.Replace("%bodytype%", this.chartype);
				File.WriteAllText(path2, str2 + text3);
			}
			try
			{
				string text4 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings\\2021Server.lua");
				string path3 = AppDomain.CurrentDomain.BaseDirectory.ToString() + "shared\\ExtraContent\\scripts\\CoreScripts\\ServerStarterScript.lua";
				text4 = text4.Replace("%bodytype%", this.chartype);
				File.WriteAllText(path3, str2 + text4);
			}
			catch
			{
			}
			string text5 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/MapPath.txt");
			if (File.Exists(text5))
			{
				string path4 = AppDomain.CurrentDomain.BaseDirectory + "Webserver/www/.127.0.0.1/asset/1818";
				if (File.Exists(path4))
				{
					File.Delete(path4);
				}
				string destFileName = AppDomain.CurrentDomain.BaseDirectory + "Webserver/www/.127.0.0.1/asset/1818";
				try
				{
					File.Copy(text5, destFileName, true);
				}
				catch (IOException ex)
				{
					Console.WriteLine(ex.Message);
				}
				string path5 = AppDomain.CurrentDomain.BaseDirectory + "Webserver/www/.localhost/asset/1818";
				if (File.Exists(path5))
				{
					File.Delete(path5);
				}
				string destFileName2 = AppDomain.CurrentDomain.BaseDirectory + "Webserver/www/.localhost/asset/1818";
				try
				{
					File.Copy(text5, destFileName2, true);
				}
				catch (IOException ex2)
				{
					Console.WriteLine(ex2.Message);
				}
				string path6 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/place.rbxl";
				if (File.Exists(path6))
				{
					File.Delete(path6);
				}
				string destFileName3 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/place.rbxl";
				try
				{
					File.Copy(text5, destFileName3, true);
				}
				catch (IOException ex3)
				{
					Console.WriteLine(ex3.Message);
				}
				string path7 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/1818";
				if (File.Exists(path7))
				{
					File.Delete(path7);
				}
				string destFileName4 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/1818";
				try
				{
					File.Copy(text5, destFileName4, true);
				}
				catch (IOException ex4)
				{
					Console.WriteLine(ex4.Message);
				}
				string path8 = AppDomain.CurrentDomain.BaseDirectory + "Clients\\2014M\\content\\temp.rbxl";
				if (File.Exists(path8))
				{
					File.Delete(path8);
				}
				string destFileName5 = AppDomain.CurrentDomain.BaseDirectory + "Clients\\2014M\\content\\temp.rbxl";
				try
				{
					File.Copy(text5, destFileName5, true);
				}
				catch (IOException ex5)
				{
					Console.WriteLine(ex5.Message);
				}
			}
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/HostPort.txt"
			}.FileName))
			{
				streamWriter.WriteLine(this.textBox4.Text);
			}
			string text6 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Fix.ini");
			if (this.currentclient == "2022M")
			{
				string text7 = "";
				DialogResult dialogResult = MessageBox.Show("Would you like to host without filtering? (Clicking no is insecure!)", "Roblox Launcher", MessageBoxButtons.YesNo);
				if (dialogResult == DialogResult.Yes)
				{
					text7 = "_G.FilteringEnabled=true";
				}
				else if (dialogResult == DialogResult.No)
				{
					text7 = "_G.FilteringEnabled=false";
				}
				string value = string.Concat(new string[]
				{
					"<roblox xmlns:xmime=",
					text6,
					"http://www.w3.org/2005/05/xmlmime",
					text6,
					" xmlns:xsi=",
					text6,
					"http://www.w3.org/2001/XMLSchema-instance",
					text6,
					" xsi:noNamespaceSchemaLocation=",
					text6,
					"http://www.localhost//roblox.xsd",
					text6,
					" version=",
					text6,
					"4",
					text6,
					">\r\n    <External>null</External>\r\n    <External>nil</External>\r\n    <Item class=",
					text6,
					"Script",
					text6,
					" referent=",
					text6,
					"RBXA9BF459DE88842189FF810D1F9615061",
					text6,
					">\r\n\t\t<Properties>\r\n\t\t\t<bool name =",
					text6,
					"Disabled",
					text6,
					">false</bool>\r\n            <Content name=",
					text6,
					"LinkedSource",
					text6,
					"><null></null></Content>\r\n\t\t\t<string name =",
					text6,
					"Name",
					text6,
					">Script</string>\r\n            <string name=",
					text6,
					"ScriptGuid",
					text6,
					">{1166F3A8-F70B-4DAF-B7C6-3C89D8BBC049}</string>\r\n\t\t\t<ProtectedString name=",
					text6,
					"Source",
					text6,
					"><![CDATA[",
					text7,
					"]]></ProtectedString>\r\n            <BinaryString name=",
					text6,
					"Tags",
					text6,
					"></BinaryString>\r\n\t\t</Properties>\r\n\t</Item>\r\n</roblox>"
				});
				using (StreamWriter streamWriter2 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "shared/content/server.rbxmx"
				}.FileName))
				{
					streamWriter2.WriteLine(value);
				}
				string text8 = "\"";
				string rbxexe = AppDomain.CurrentDomain.BaseDirectory + "Clients/2022M/RobloxStudioBeta.exe";
				string text9 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/place.rbxl";
				string mapname = "place.rbxl";
				string args = string.Concat(new string[]
				{
					text8,
					"\" -localPlaceFile ",
					text6,
					text9,
					text6,
					" -task StartServer -port ",
					this.textBox4.Text,
					text8
				});
				Form1.OpenClient(rbxexe, args, mapname, false);
				return;
			}
			if (this.currentclient == "2016L" || this.currentclient == "2015L")
			{
				string text10 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/shared/test.txt");
				text10 = text10.Replace("%bodytype%", this.chartype);
				text10 = text10.Replace("%port%", this.textBox4.Text);
				using (StreamWriter streamWriter3 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "/shared/gameserver.txt"
				}.FileName))
				{
					streamWriter3.WriteLine(text10);
				}
				Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "shared\\" + this.currentclient + ".bat")
				{
					UseShellExecute = true
				});
				return;
			}
			if (this.currentclient == "2017M")
			{
				Form1.ExecuteCommand("start shared\\" + this.currentclient + ".bat -Console -verbose -placeid:1818 -port 64989");
				this.started2017 = false;
				return;
			}
			if (this.currentclient == "2021E")
			{
				string text11 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/gameserverraw.json");
				text11 = text11.Replace("%port%", this.textBox4.Text);
				using (StreamWriter streamWriter4 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "shared\\gameserver.json"
				}.FileName))
				{
					streamWriter4.WriteLine(text11);
				}
				Form1.ExecuteCommand("start shared\\" + this.currentclient + ".bat");
				return;
			}
			if (this.currentclient == "2014M")
			{
				Form1.ExecuteCommand(string.Concat(new string[]
				{
					"start Clients\\2014M\\RCCService.exe -a ",
					text6,
					"http://localhost/www.civdefn.tk/",
					text6,
					" -j ",
					text6,
					"http://localhost/www.civdefn.tk/game/host.php?port=",
					this.textBox4.Text,
					text6,
					" -t ",
					text6,
					"1",
					text6
				}));
				return;
			}
			if (this.currentclient == "2013L")
			{
				Form1.ExecuteCommand(string.Concat(new string[]
				{
					"start Clients\\2013L\\RCCService.exe -a ",
					text6,
					"http://localhost/www.civdefn.tk/",
					text6,
					" -j ",
					text6,
					"http://localhost/www.civdefn.tk/game/host.php?port=",
					this.textBox4.Text,
					text6,
					" -t ",
					text6,
					"1",
					text6
				}));
				return;
			}
			if (this.currentclient == "2008M")
			{
				string text12 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/shared/2008hostoriginal.txt");
				text12 = text12.Replace("%port%", this.textBox4.Text);
				using (StreamWriter streamWriter5 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "/shared/2008host.txt"
				}.FileName))
				{
					streamWriter5.WriteLine(text12);
				}
				Form1.ExecuteCommand("start Clients\\" + this.currentclient + "\\RCCService\\RCCService.bat");
				this.started2008 = false;
				return;
			}
			if (this.currentclient == "2013")
			{
				string text13 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/shared/2008hostoriginal.txt");
				text13 = text13.Replace("%port%", this.textBox4.Text);
				using (StreamWriter streamWriter6 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "/Clients/2013/Player/content/2014host.txt"
				}.FileName))
				{
					streamWriter6.WriteLine(text13);
				}
				Form1.ExecuteCommand("start Clients\\" + this.currentclient + "\\Player\\RCCService.bat");
				return;
			}
			try
			{
				string text14 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/gameserverraw.json");
				text14 = text14.Replace("%port%", this.textBox4.Text);
				using (StreamWriter streamWriter7 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "shared/gameserver.json"
				}.FileName))
				{
					streamWriter7.WriteLine(text14);
				}
				Form1.ExecuteCommand("start shared\\" + this.currentclient + ".bat");
			}
			catch
			{
				string text15 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/gameserverraw.json");
				text15 = text15.Replace("%port%", this.textBox4.Text);
				using (StreamWriter streamWriter8 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "shared/gameserver.json"
				}.FileName))
				{
					streamWriter8.WriteLine(text15);
				}
				Form1.ExecuteCommand(string.Concat(new string[]
				{
					"start shared/",
					this.currentclient,
					".exe -Console -verbose -placeid:1818 -localtest ",
					text6,
					"gameserver.json",
					text6,
					"  -port 64989"
				}));
			}
		}

		// Token: 0x06000041 RID: 65 RVA: 0x0000513C File Offset: 0x0000333C
		private static string RemoveWhitespace(string input)
		{
			return new string((from c in input.ToCharArray()
			where !char.IsWhiteSpace(c)
			select c).ToArray<char>());
		}

		// Token: 0x06000042 RID: 66 RVA: 0x00005174 File Offset: 0x00003374
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
				Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini")),
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
				text3 = Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini"));
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
					FileName = AppDomain.CurrentDomain.BaseDirectory + "shared/ExtraContent/test.rbxmx"
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
			if (this.currentclient == "2015L")
			{
				Form1.ExecuteCommand(string.Concat(new string[]
				{
					"start shared/2015Player.exe -a ",
					text2,
					"http://localhost/login/negotiate.ashx",
					text2,
					" -j ",
					text2,
					"http://localhost/game/placelaunchrrr.php/?placeid=1818&ip=",
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
			if (this.currentclient == "2016L")
			{
				Form1.ExecuteCommand(string.Concat(new string[]
				{
					"start shared/2016Player.exe -a ",
					text2,
					"http://localhost/login/negotiate.ashx",
					text2,
					" -j ",
					text2,
					"http://localhost/game/placelaunchrrr.php/?placeid=1818&ip=",
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
					"start shared/2017Player.exe -a ",
					text2,
					"http://localhost/login/negotiate.ashx",
					text2,
					" -j ",
					text2,
					"http://localhost/game/join.php/?placeid=1818&ip=",
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
			if (this.currentclient == "2014M")
			{
				text3 = text3.Replace("localhost", "localhost/www.civdefn.tk/");
				Form1.ExecuteCommand(string.Concat(new string[]
				{
					"start Clients\\2014M\\RobloxPlayerBeta.exe -a ",
					text2,
					"http://localhost/www.civdefn.tk/",
					text2,
					" -j ",
					text2,
					"http://localhost/www.civdefn.tk/game/join.php?port=",
					this.textBox4.Text,
					"&app=",
					text3,
					"&ip=",
					this.textBox3.Text,
					"&username=",
					this.textBox1.Text,
					"&id=",
					this.num.ToString(),
					"&mode=1",
					text2,
					" -t ",
					text2,
					"1",
					text2
				}));
				return;
			}
			if (this.currentclient == "2013L")
			{
				text3 = text3.Replace("localhost", "localhost/www.civdefn.tk/");
				Form1.ExecuteCommand(string.Concat(new string[]
				{
					"start Clients\\2013L\\RobloxPlayerBeta.exe -a ",
					text2,
					"http://localhost/www.civdefn.tk/",
					text2,
					" -j ",
					text2,
					"http://localhost/www.civdefn.tk/game/join.php?port=",
					this.textBox4.Text,
					"&app=",
					text3,
					"&ip=",
					this.textBox3.Text,
					"&username=",
					this.textBox1.Text,
					"&id=",
					this.num.ToString(),
					"&mode=1",
					text2,
					" -t ",
					text2,
					"1",
					text2
				}));
				return;
			}
			if (this.currentclient == "2021E")
			{
				text3 = text3.Replace("1111111", "");
				Form1.ExecuteCommand(string.Concat(new string[]
				{
					"start Clients\\2021E\\RCCService\\RobloxPlayerBeta.exe -a ",
					text2,
					"http://localhost/2021/login/negotiate.ashx",
					text2,
					" -j ",
					text2,
					"http://localhost/2021/game/placelauncher.ashx?placeid=1818&ip=",
					this.textBox3.Text,
					"&user=",
					this.textBox1.Text,
					"&port=",
					this.textBox2.Text,
					"&id=",
					this.num.ToString(),
					"&app=",
					text3,
					text2,
					" -t ",
					text2,
					"1",
					text2
				}));
				return;
			}
			if (this.currentclient == "2008M")
			{
				string text6 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Clients/2008M/join.txt");
				text6 = text6.Replace("%port%", this.textBox4.Text);
				text6 = text6.Replace("%ip%", text2 + this.textBox3.Text + text2);
				text6 = text6.Replace("%name%", text2 + this.textBox1.Text + text2);
				text6 = text6.Replace("%id%", this.num.ToString());
				text3 = string.Concat(new string[]
				{
					Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini")),
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
				text6 = "charapp = [[" + text3 + "]]  \n" + text6;
				using (StreamWriter streamWriter5 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "Clients/2008M/Player/content/join.txt"
				}.FileName))
				{
					streamWriter5.WriteLine(text6);
				}
				Form1.ExecuteCommand("start Clients/2008M/Player/Roblox.exe -script " + text2 + "dofile('rbxasset://join.txt')" + text2);
				return;
			}
			if (this.currentclient == "2013")
			{
				string text7 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Clients/2013/join.txt");
				text7 = text7.Replace("%port%", this.textBox4.Text);
				text7 = text7.Replace("%ip%", text2 + this.textBox3.Text + text2);
				text7 = text7.Replace("%name%", text2 + this.textBox1.Text + text2);
				text7 = text7.Replace("%id%", this.num.ToString());
				text3 = string.Concat(new string[]
				{
					Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini")),
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
				text7 = "charapp = [[" + text3 + "]]  \n" + text7;
				using (StreamWriter streamWriter6 = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "Clients/2013/Player/content/join.txt"
				}.FileName))
				{
					streamWriter6.WriteLine(text7);
				}
				Form1.ExecuteCommand("start Clients/2013/Player/Roblox.exe -script " + text2 + "dofile('rbxasset://join.txt')" + text2);
				return;
			}
			text3 = text3.Replace("1111111", "");
			Form1.ExecuteCommand(string.Concat(new string[]
			{
				"start Clients/",
				this.currentclient,
				"/Player/RobloxPlayerBeta.exe -a ",
				text2,
				"http://localhost/login/negotiate.ashx",
				text2,
				" -j ",
				text2,
				"http://localhost/game/placelauncher.ashx?&year=2018&placeid=1818&ip=",
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

		// Token: 0x06000043 RID: 67 RVA: 0x0000607C File Offset: 0x0000427C
		private void Form1_Shown(object sender, EventArgs e)
		{
			if (!Directory.Exists(AppDomain.CurrentDomain.BaseDirectory + "\\WebServer"))
			{
				return;
			}
			if (!File.Exists(AppDomain.CurrentDomain.BaseDirectory + "WebServer/Start.bat"))
			{
				return;
			}
			Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "WebServer/Start.bat")
			{
				UseShellExecute = true,
				WindowStyle = ProcessWindowStyle.Minimized
			});
			string text = Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/username.txt"));
			string s = text.GetHashCode().ToString().Remove(0, 1);
			this.num = int.Parse(s);
			this.textBox1.Text = text;
			text = Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/ip.txt"));
			this.textBox3.Text = text;
			text = Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/clientport.txt"));
			this.textBox2.Text = text;
			text = Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/HostPort.txt"));
			this.textBox4.Text = text;
			text = Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/SelectedClient.txt"));
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
			text = Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyType.txt"));
			this.listBox2.SetSelected(this.listBox2.FindString(text), true);
			text = Form1.RemoveWhitespace(File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "Settings/assetsaving/Enabled.txt"));
			this.listBox3.SetSelected(this.listBox3.FindString(text), true);
		}

		// Token: 0x06000044 RID: 68 RVA: 0x00006328 File Offset: 0x00004528
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
				using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
				{
					FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/MapPath.txt"
				}.FileName))
				{
					streamWriter.WriteLine(fileName);
				}
				if (File.Exists(fileName))
				{
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
					string path2 = AppDomain.CurrentDomain.BaseDirectory + "Webserver/www/.localhost/asset/1818";
					if (File.Exists(path2))
					{
						File.Delete(path2);
					}
					string destFileName2 = AppDomain.CurrentDomain.BaseDirectory + "Webserver/www/.localhost/asset/1818";
					try
					{
						File.Copy(fileName, destFileName2, true);
					}
					catch (IOException ex2)
					{
						Console.WriteLine(ex2.Message);
					}
					string path3 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/place.rbxl";
					if (File.Exists(path3))
					{
						File.Delete(path3);
					}
					string destFileName3 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/place.rbxl";
					try
					{
						File.Copy(fileName, destFileName3, true);
					}
					catch (IOException ex3)
					{
						Console.WriteLine(ex3.Message);
					}
					string path4 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/1818";
					if (File.Exists(path4))
					{
						File.Delete(path4);
					}
					string destFileName4 = AppDomain.CurrentDomain.BaseDirectory + "shared/content/1818";
					try
					{
						File.Copy(fileName, destFileName4, true);
					}
					catch (IOException ex4)
					{
						Console.WriteLine(ex4.Message);
					}
					string path5 = AppDomain.CurrentDomain.BaseDirectory + "Clients\\2014M\\content\\temp.rbxl";
					if (File.Exists(path5))
					{
						File.Delete(path5);
					}
					string destFileName5 = AppDomain.CurrentDomain.BaseDirectory + "Clients\\2014M\\content\\temp.rbxl";
					try
					{
						File.Copy(fileName, destFileName5, true);
					}
					catch (IOException ex5)
					{
						Console.WriteLine(ex5.Message);
					}
				}
			}
		}

		// Token: 0x06000045 RID: 69 RVA: 0x000065A4 File Offset: 0x000047A4
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
			using (StreamWriter streamWriter8 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyType.txt"
			}.FileName))
			{
				streamWriter8.Write(this.chartype);
			}
			using (StreamWriter streamWriter9 = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/assetsaving/Enabled.txt"
			}.FileName))
			{
				streamWriter9.Write(this.assetsaving);
			}
			try
			{
				Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "WebServer/kill.bat")
				{
					UseShellExecute = true,
					WindowStyle = ProcessWindowStyle.Minimized
				});
			}
			catch
			{
			}
		}

		// Token: 0x06000046 RID: 70 RVA: 0x000068C8 File Offset: 0x00004AC8
		private void textBox1_TextChanged(object sender, EventArgs e)
		{
			try
			{
				string s = this.textBox1.Text.GetHashCode().ToString().Remove(0, 1);
				this.num = int.Parse(s);
			}
			catch (Exception)
			{
			}
		}

		// Token: 0x06000047 RID: 71 RVA: 0x00006918 File Offset: 0x00004B18
		private void textBox4_TextChanged(object sender, EventArgs e)
		{
		}

		// Token: 0x06000048 RID: 72 RVA: 0x0000691A File Offset: 0x00004B1A
		private void Form1_FormClosed(object sender, FormClosedEventArgs e)
		{
		}

		// Token: 0x06000049 RID: 73 RVA: 0x0000691C File Offset: 0x00004B1C
		private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
		{
			string text = this.listBox1.SelectedItem.ToString();
			this.currentclient = text;
		}

		// Token: 0x0600004A RID: 74 RVA: 0x00006941 File Offset: 0x00004B41
		private void checkedListBox1_SelectedIndexChanged(object sender, EventArgs e)
		{
		}

		// Token: 0x0600004B RID: 75 RVA: 0x00006944 File Offset: 0x00004B44
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

		// Token: 0x0600004C RID: 76 RVA: 0x00006A84 File Offset: 0x00004C84
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

		// Token: 0x0600004D RID: 77 RVA: 0x00006BC4 File Offset: 0x00004DC4
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

		// Token: 0x0600004E RID: 78 RVA: 0x00006D04 File Offset: 0x00004F04
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

		// Token: 0x0600004F RID: 79 RVA: 0x00006E43 File Offset: 0x00005043
		private void button4_Click(object sender, EventArgs e)
		{
			Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "WebServer/Start.bat")
			{
				UseShellExecute = true,
				WindowStyle = ProcessWindowStyle.Minimized
			});
		}

		// Token: 0x06000050 RID: 80 RVA: 0x00006E72 File Offset: 0x00005072
		private void button5_Click(object sender, EventArgs e)
		{
			Process.Start(new ProcessStartInfo(AppDomain.CurrentDomain.BaseDirectory + "WebServer/kill.bat")
			{
				UseShellExecute = true,
				WindowStyle = ProcessWindowStyle.Minimized
			});
		}

		// Token: 0x06000051 RID: 81 RVA: 0x00006EA4 File Offset: 0x000050A4
		private void pictureBox5_Click(object sender, EventArgs e)
		{
			if (!File.Exists(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/HeadColor.txt"))
			{
				File.Create(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/HeadColor.txt");
			}
			this.selectedbodypart = "Head";
			this.pictureBox5.BorderStyle = BorderStyle.Fixed3D;
			this.pictureBox6.BorderStyle = BorderStyle.None;
			this.pictureBox7.BorderStyle = BorderStyle.None;
			this.pictureBox8.BorderStyle = BorderStyle.None;
			this.pictureBox9.BorderStyle = BorderStyle.None;
			this.pictureBox10.BorderStyle = BorderStyle.None;
		}

		// Token: 0x06000052 RID: 82 RVA: 0x00006F3C File Offset: 0x0000513C
		private void pictureBox6_Click(object sender, EventArgs e)
		{
			if (!File.Exists(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/TorsoColor.txt"))
			{
				File.Create(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/TorsoColor.txt");
			}
			this.selectedbodypart = "Torso";
			this.pictureBox5.BorderStyle = BorderStyle.None;
			this.pictureBox6.BorderStyle = BorderStyle.Fixed3D;
			this.pictureBox7.BorderStyle = BorderStyle.None;
			this.pictureBox8.BorderStyle = BorderStyle.None;
			this.pictureBox9.BorderStyle = BorderStyle.None;
			this.pictureBox10.BorderStyle = BorderStyle.None;
		}

		// Token: 0x06000053 RID: 83 RVA: 0x00006FD4 File Offset: 0x000051D4
		private void pictureBox7_Click(object sender, EventArgs e)
		{
			if (!File.Exists(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/LeftArmColor.txt"))
			{
				File.Create(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/LeftArmColor.txt");
			}
			this.selectedbodypart = "Left Arm";
			this.pictureBox5.BorderStyle = BorderStyle.None;
			this.pictureBox6.BorderStyle = BorderStyle.None;
			this.pictureBox7.BorderStyle = BorderStyle.Fixed3D;
			this.pictureBox8.BorderStyle = BorderStyle.None;
			this.pictureBox9.BorderStyle = BorderStyle.None;
			this.pictureBox10.BorderStyle = BorderStyle.None;
		}

		// Token: 0x06000054 RID: 84 RVA: 0x0000706C File Offset: 0x0000526C
		private void pictureBox8_Click(object sender, EventArgs e)
		{
			if (!File.Exists(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/RightArmColor.txt"))
			{
				File.Create(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/RightArmColor.txt");
			}
			this.selectedbodypart = "Right Arm";
			this.pictureBox5.BorderStyle = BorderStyle.None;
			this.pictureBox6.BorderStyle = BorderStyle.None;
			this.pictureBox7.BorderStyle = BorderStyle.None;
			this.pictureBox8.BorderStyle = BorderStyle.Fixed3D;
			this.pictureBox9.BorderStyle = BorderStyle.None;
			this.pictureBox10.BorderStyle = BorderStyle.None;
		}

		// Token: 0x06000055 RID: 85 RVA: 0x00007104 File Offset: 0x00005304
		private void pictureBox9_Click(object sender, EventArgs e)
		{
			if (!File.Exists(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/LeftLegColor.txt"))
			{
				File.Create(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/LeftLegColor.txt");
			}
			this.selectedbodypart = "Left Leg";
			this.pictureBox5.BorderStyle = BorderStyle.None;
			this.pictureBox6.BorderStyle = BorderStyle.None;
			this.pictureBox7.BorderStyle = BorderStyle.None;
			this.pictureBox8.BorderStyle = BorderStyle.None;
			this.pictureBox9.BorderStyle = BorderStyle.Fixed3D;
			this.pictureBox10.BorderStyle = BorderStyle.None;
		}

		// Token: 0x06000056 RID: 86 RVA: 0x0000719C File Offset: 0x0000539C
		private void pictureBox10_Click(object sender, EventArgs e)
		{
			if (!File.Exists(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/RightLegColor.txt"))
			{
				File.Create(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyColors/RightLegColor.txt");
			}
			this.selectedbodypart = "Right Leg";
			this.pictureBox5.BorderStyle = BorderStyle.None;
			this.pictureBox6.BorderStyle = BorderStyle.None;
			this.pictureBox7.BorderStyle = BorderStyle.None;
			this.pictureBox8.BorderStyle = BorderStyle.None;
			this.pictureBox9.BorderStyle = BorderStyle.None;
			this.pictureBox10.BorderStyle = BorderStyle.Fixed3D;
		}

		// Token: 0x06000057 RID: 87 RVA: 0x00007231 File Offset: 0x00005431
		public static string ReplaceWhitespace(string input, string replacement)
		{
			return Form1.sWhitespace.Replace(input, replacement);
		}

		// Token: 0x06000058 RID: 88 RVA: 0x00007240 File Offset: 0x00005440
		private void pictureBox11_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=607785314";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x06000059 RID: 89 RVA: 0x000072D0 File Offset: 0x000054D0
		private void button6_Click(object sender, EventArgs e)
		{
			this.label5.Text = "Cleared!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine("http://localhost/charscript/Custom.php?hat=0");
			}
		}

		// Token: 0x0600005A RID: 90 RVA: 0x00007340 File Offset: 0x00005540
		private void pictureBox12_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=398633584";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x0600005B RID: 91 RVA: 0x000073D0 File Offset: 0x000055D0
		private void pictureBox13_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=398634487";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x0600005C RID: 92 RVA: 0x00007460 File Offset: 0x00005660
		private void pictureBox14_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=398635338";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x0600005D RID: 93 RVA: 0x000074F0 File Offset: 0x000056F0
		private void pictureBox15_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=3670737444";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x0600005E RID: 94 RVA: 0x00007580 File Offset: 0x00005780
		private void pictureBox17_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=6111376717";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x0600005F RID: 95 RVA: 0x00007610 File Offset: 0x00005810
		private void pictureBox18_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=6087965870";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x06000060 RID: 96 RVA: 0x000076A0 File Offset: 0x000058A0
		private void pictureBox19_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=451221329";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x06000061 RID: 97 RVA: 0x00007730 File Offset: 0x00005930
		private void pictureBox20_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=2956239660";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x06000062 RID: 98 RVA: 0x000077C0 File Offset: 0x000059C0
		private void pictureBox21_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=212967757";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x06000063 RID: 99 RVA: 0x00007850 File Offset: 0x00005A50
		private void pictureBox22_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=63690008";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x06000064 RID: 100 RVA: 0x000078E0 File Offset: 0x00005AE0
		private void pictureBox23_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=1103003368";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x06000065 RID: 101 RVA: 0x00007970 File Offset: 0x00005B70
		private void button7_Click(object sender, EventArgs e)
		{
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=1111111" + this.textBox5.Text;
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x06000066 RID: 102 RVA: 0x00007A0C File Offset: 0x00005C0C
		private void pictureBox16_Click(object sender, EventArgs e)
		{
			try
			{
				if (!File.Exists(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini"))
				{
					File.Create(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini");
				}
			}
			catch
			{
			}
			string value = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Appearence.ini") + ";http://localhost/asset/?id=398635081";
			this.label5.Text = "Equipped!";
			using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
			{
				FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/Appearence.ini"
			}.FileName))
			{
				streamWriter.WriteLine(value);
			}
		}

		// Token: 0x06000067 RID: 103 RVA: 0x00007AE0 File Offset: 0x00005CE0
		private void button8_Click(object sender, EventArgs e)
		{
			try
			{
				string text = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/MapPath.txt");
				if (File.Exists(text))
				{
					string path = AppDomain.CurrentDomain.BaseDirectory + "/Webserver/www/.127.0.0.1/asset/1818";
					if (File.Exists(path))
					{
						File.Delete(path);
					}
					string destFileName = AppDomain.CurrentDomain.BaseDirectory + "/Webserver/www/.127.0.0.1/asset/1818";
					try
					{
						File.Copy(text, destFileName, true);
					}
					catch (IOException ex)
					{
						Console.WriteLine(ex.Message);
					}
					string path2 = AppDomain.CurrentDomain.BaseDirectory + "/Webserver/www/.localhost/asset/1818";
					if (File.Exists(path2))
					{
						File.Delete(path2);
					}
					string destFileName2 = AppDomain.CurrentDomain.BaseDirectory + "/Webserver/www/.localhost/asset/1818";
					try
					{
						File.Copy(text, destFileName2, true);
					}
					catch (IOException ex2)
					{
						Console.WriteLine(ex2.Message);
					}
					string path3 = AppDomain.CurrentDomain.BaseDirectory + "/shared/content/place.rbxl";
					if (File.Exists(path3))
					{
						File.Delete(path3);
					}
					string destFileName3 = AppDomain.CurrentDomain.BaseDirectory + "/shared/content/place.rbxl";
					try
					{
						File.Copy(text, destFileName3, true);
					}
					catch (IOException ex3)
					{
						Console.WriteLine(ex3.Message);
					}
					string path4 = AppDomain.CurrentDomain.BaseDirectory + "/shared/content/1818";
					if (File.Exists(path4))
					{
						File.Delete(path4);
					}
					string destFileName4 = AppDomain.CurrentDomain.BaseDirectory + "/shared/content/1818";
					try
					{
						File.Copy(text, destFileName4, true);
					}
					catch (IOException ex4)
					{
						Console.WriteLine(ex4.Message);
					}
					string path5 = AppDomain.CurrentDomain.BaseDirectory + "\\Clients\\2014M\\content\\temp.rbxl";
					if (File.Exists(path5))
					{
						File.Delete(path5);
					}
					string destFileName5 = AppDomain.CurrentDomain.BaseDirectory + "\\Clients\\2014M\\content\\temp.rbxl";
					try
					{
						File.Copy(text, destFileName5, true);
					}
					catch (IOException ex5)
					{
						Console.WriteLine(ex5.Message);
					}
					string text2 = File.ReadAllText(AppDomain.CurrentDomain.BaseDirectory + "/Settings/Fix.ini");
					string text3 = "_G.FilteringEnabled=true";
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
						"Script",
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
						">Script</string>\r\n            <string name=",
						text2,
						"ScriptGuid",
						text2,
						">{1166F3A8-F70B-4DAF-B7C6-3C89D8BBC049}</string>\r\n\t\t\t<ProtectedString name=",
						text2,
						"Source",
						text2,
						"><![CDATA[",
						text3,
						"]]></ProtectedString>\r\n            <BinaryString name=",
						text2,
						"Tags",
						text2,
						"></BinaryString>\r\n\t\t</Properties>\r\n\t</Item>\r\n</roblox>"
					});
					using (StreamWriter streamWriter = new StreamWriter(new SaveFileDialog
					{
						FileName = AppDomain.CurrentDomain.BaseDirectory + "//shared/content/server.rbxmx"
					}.FileName))
					{
						streamWriter.WriteLine(value);
					}
					string text4 = "\"";
					string str = AppDomain.CurrentDomain.BaseDirectory + "\\Clients\\2022M\\RobloxStudioBeta.exe";
					AppDomain.CurrentDomain.BaseDirectory + "\\shared\\content\\place.rbxl";
					string str2 = " -localPlaceFile " + text4 + text + text4;
					string str3 = text4 + str + text4 + str2;
					using (StreamWriter streamWriter2 = new StreamWriter(new SaveFileDialog
					{
						FileName = AppDomain.CurrentDomain.BaseDirectory + "Settings/EditMap.bat"
					}.FileName))
					{
						streamWriter2.WriteLine(str3 + "\n exit");
					}
					Form1.ExecuteCommand("start Settings\\EditMap.bat");
				}
			}
			catch
			{
			}
		}

		// Token: 0x06000068 RID: 104 RVA: 0x00008014 File Offset: 0x00006214
		private void tabPage2_Click(object sender, EventArgs e)
		{
		}

		// Token: 0x06000069 RID: 105 RVA: 0x00008018 File Offset: 0x00006218
		private void listBox2_SelectedIndexChanged(object sender, EventArgs e)
		{
			if (!File.Exists(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyType.txt"))
			{
				File.Create(AppDomain.CurrentDomain.BaseDirectory + "Settings/BodyType.txt");
			}
			this.chartype = this.listBox2.SelectedItem.ToString();
		}

		// Token: 0x0600006A RID: 106 RVA: 0x00008070 File Offset: 0x00006270
		private void label12_Click(object sender, EventArgs e)
		{
		}

		// Token: 0x0600006B RID: 107 RVA: 0x00008074 File Offset: 0x00006274
		private void listBox3_SelectedIndexChanged(object sender, EventArgs e)
		{
			string text = this.listBox3.SelectedItem.ToString();
			this.assetsaving = text;
			if (this.assetsaving == "true")
			{
				string fullPath = Path.GetFullPath(AppDomain.CurrentDomain.BaseDirectory + "\\Webserver\\www");
				DirectoryInfo target = new DirectoryInfo(Path.GetFullPath(AppDomain.CurrentDomain.BaseDirectory + "\\Webserver\\www"));
				DirectoryInfo source = new DirectoryInfo(Path.GetFullPath(AppDomain.CurrentDomain.BaseDirectory + "\\Settings\\assetsaving\\SaveAssets"));
				if (Directory.Exists(fullPath))
				{
					Form1.CopyFilesRecursively(source, target);
				}
			}
			if (this.assetsaving == "false")
			{
				string fullPath2 = Path.GetFullPath(AppDomain.CurrentDomain.BaseDirectory + "\\Webserver\\www");
				DirectoryInfo target2 = new DirectoryInfo(Path.GetFullPath(AppDomain.CurrentDomain.BaseDirectory + "\\Webserver\\www"));
				DirectoryInfo source2 = new DirectoryInfo(Path.GetFullPath(AppDomain.CurrentDomain.BaseDirectory + "\\Settings\\assetsaving\\DontSave"));
				if (Directory.Exists(fullPath2))
				{
					Form1.CopyFilesRecursively(source2, target2);
				}
			}
		}

		// Token: 0x0600006C RID: 108 RVA: 0x00008189 File Offset: 0x00006389
		private void tabPage1_Click(object sender, EventArgs e)
		{
		}

		// Token: 0x0600006D RID: 109 RVA: 0x0000818B File Offset: 0x0000638B
		private void textBox3_TextChanged(object sender, EventArgs e)
		{
		}

		// Token: 0x0600006E RID: 110 RVA: 0x0000818D File Offset: 0x0000638D
		private void label1_Click(object sender, EventArgs e)
		{
		}

		// Token: 0x0600006F RID: 111 RVA: 0x0000818F File Offset: 0x0000638F
		private void label2_Click(object sender, EventArgs e)
		{
		}

		// Token: 0x06000070 RID: 112 RVA: 0x00008191 File Offset: 0x00006391
		private void label3_Click(object sender, EventArgs e)
		{
		}

		// Token: 0x06000071 RID: 113 RVA: 0x00008193 File Offset: 0x00006393
		private void ExploitName_Click(object sender, EventArgs e)
		{
		}

		// Token: 0x06000072 RID: 114 RVA: 0x00008195 File Offset: 0x00006395
		private void ExitButton_Click(object sender, EventArgs e)
		{
		}

		// Token: 0x06000073 RID: 115 RVA: 0x00008197 File Offset: 0x00006397
		private void button10_Click(object sender, EventArgs e)
		{
			base.Close();
		}

		// Token: 0x06000074 RID: 116 RVA: 0x0000819F File Offset: 0x0000639F
		private void button11_Click(object sender, EventArgs e)
		{
			base.WindowState = FormWindowState.Minimized;
		}

		// Token: 0x06000075 RID: 117 RVA: 0x000081A8 File Offset: 0x000063A8
		private void panel1_Paint(object sender, PaintEventArgs e)
		{
		}

		// Token: 0x06000076 RID: 118 RVA: 0x000081AA File Offset: 0x000063AA
		private void panel1_MouseDown(object sender, MouseEventArgs e)
		{
			this._dragging = true;
			this._start_point = new Point(e.X, e.Y);
		}

		// Token: 0x06000077 RID: 119 RVA: 0x000081CA File Offset: 0x000063CA
		private void panel1_MouseUp(object sender, MouseEventArgs e)
		{
			this._dragging = false;
		}

		// Token: 0x06000078 RID: 120 RVA: 0x000081D4 File Offset: 0x000063D4
		private void panel1_MouseMove(object sender, MouseEventArgs e)
		{
			if (this._dragging)
			{
				Point point = base.PointToScreen(e.Location);
				base.Location = new Point(point.X - this._start_point.X, point.Y - this._start_point.Y);
			}
		}

		// Token: 0x06000079 RID: 121 RVA: 0x00008227 File Offset: 0x00006427
		private void button14_Click(object sender, EventArgs e)
		{
			base.Close();
		}

		// Token: 0x0600007A RID: 122 RVA: 0x0000822F File Offset: 0x0000642F
		private void button13_Click(object sender, EventArgs e)
		{
			base.WindowState = FormWindowState.Minimized;
		}

		// Token: 0x0600007B RID: 123 RVA: 0x00008238 File Offset: 0x00006438
		private void tabControl1_DrawItem(object sender, DrawItemEventArgs e)
		{
			Rectangle clientRectangle = this.tabControl1.ClientRectangle;
			StringFormat stringFormat = new StringFormat();
			stringFormat.LineAlignment = StringAlignment.Center;
			stringFormat.Alignment = StringAlignment.Center;
			SolidBrush brush = new SolidBrush(Color.FromArgb(40, 40, 40));
			SolidBrush brush2 = new SolidBrush(Color.White);
			e.Graphics.FillRectangle(brush, clientRectangle);
			Font font = new Font(new FontFamily("Segoe UI"), 12f, FontStyle.Regular, GraphicsUnit.Point);
			Brush brush3 = new SolidBrush(Color.FromArgb(30, 30, 30));
			for (int i = 0; i < this.tabControl1.TabPages.Count; i++)
			{
				bool flag = this.tabControl1.SelectedIndex == i;
				Rectangle tabRect = this.tabControl1.GetTabRect(i);
				RectangleF layoutRectangle = this.tabControl1.GetTabRect(i);
				if (flag)
				{
					tabRect.Inflate(2, 5);
					e.Graphics.FillRectangle(brush3, tabRect);
					e.Graphics.DrawString(this.tabControl1.TabPages[i].Text, font, brush2, layoutRectangle, stringFormat);
				}
				else
				{
					e.Graphics.DrawString(this.tabControl1.TabPages[i].Text, font, brush2, layoutRectangle, stringFormat);
				}
			}
		}

		// Token: 0x0600007C RID: 124 RVA: 0x0000837C File Offset: 0x0000657C
		private void button10_Click_1(object sender, EventArgs e)
		{
			if (!Directory.Exists(AppDomain.CurrentDomain.BaseDirectory + "\\Clients"))
			{
				Directory.CreateDirectory(AppDomain.CurrentDomain.BaseDirectory + "\\Clients");
			}
			this.listBox1.Items.Clear();
			string[] directories = Directory.GetDirectories(AppDomain.CurrentDomain.BaseDirectory + "\\Clients");
			for (int i = 0; i < directories.Length; i++)
			{
				this.listBox1.Items.Add(Path.GetFileName(directories[i]));
			}
		}

		// Token: 0x0600007D RID: 125 RVA: 0x0000840F File Offset: 0x0000660F
		private void label6_Click(object sender, EventArgs e)
		{
		}

		// Token: 0x06000081 RID: 129 RVA: 0x0000C068 File Offset: 0x0000A268
		[CompilerGenerated]
		internal static string <timer1_Tick>g__GenerateContentXML|18_0(string baseUrl, string baseContent)
		{
			return string.Concat(new string[]
			{
				"<?xml version=\"1.0\" encoding=\"UTF - 8\"?>\r\n<SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:SOAP-ENC=\"http://schemas.xmlsoap.org/soap/encoding/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:ns2=\"http://",
				baseUrl,
				"/RCCServiceSoap\" xmlns:ns1=\"http://",
				baseUrl,
				"/\" xmlns:ns3=\"http://",
				baseUrl,
				"/RCCServiceSoap12\">\r\n\t<SOAP-ENV:Body>",
				baseContent,
				"\t</SOAP-ENV:Body>\r\n</SOAP-ENV:Envelope>"
			});
		}

		// Token: 0x06000082 RID: 130 RVA: 0x0000C0BC File Offset: 0x0000A2BC
		[CompilerGenerated]
		internal static void <timer1_Tick>g__ParseXML|18_1(string xml, string soapAction)
		{
			try
			{
				XDocument xdocument = XDocument.Parse(xml);
				uint num = <PrivateImplementationDetails>.ComputeStringHash(soapAction);
				if (num <= 976181145U)
				{
					if (num <= 524249228U)
					{
						if (num != 131588286U)
						{
							if (num != 225199403U)
							{
								if (num == 524249228U)
								{
									if (soapAction == "RenewLease")
									{
										object arg = (from x in xdocument.Descendants()
										where x.Name.LocalName == "RenewLeaseResult"
										select x).FirstOrDefault<XElement>();
										if (Form1.<>o__18.<>p__8 == null)
										{
											Form1.<>o__18.<>p__8 = CallSite<Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon>>.Create(Binder.InvokeMember(CSharpBinderFlags.ResultDiscarded, "Show", null, typeof(Form1), new CSharpArgumentInfo[]
											{
												CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.IsStaticType, null),
												CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null),
												CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
												CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
												CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null)
											}));
										}
										Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon> target = Form1.<>o__18.<>p__8.Target;
										CallSite <>p__ = Form1.<>o__18.<>p__8;
										Type typeFromHandle = typeof(MessageBox);
										if (Form1.<>o__18.<>p__7 == null)
										{
											Form1.<>o__18.<>p__7 = CallSite<Func<CallSite, object, object>>.Create(Binder.InvokeMember(CSharpBinderFlags.None, "ToString", null, typeof(Form1), new CSharpArgumentInfo[]
											{
												CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
											}));
										}
										Func<CallSite, object, object> target2 = Form1.<>o__18.<>p__7.Target;
										CallSite <>p__2 = Form1.<>o__18.<>p__7;
										if (Form1.<>o__18.<>p__6 == null)
										{
											Form1.<>o__18.<>p__6 = CallSite<Func<CallSite, object, object>>.Create(Binder.GetMember(CSharpBinderFlags.None, "FirstNode", typeof(Form1), new CSharpArgumentInfo[]
											{
												CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
											}));
										}
										target(<>p__, typeFromHandle, target2(<>p__2, Form1.<>o__18.<>p__6.Target(Form1.<>o__18.<>p__6, arg)), "RenewLease Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
										goto IL_DFC;
									}
								}
							}
							else if (soapAction == "DiagEx")
							{
								object arg = (from x in xdocument.Descendants()
								where x.Name.LocalName == "DiagExResult"
								select x).FirstOrDefault<XElement>();
								if (Form1.<>o__18.<>p__10 == null)
								{
									Form1.<>o__18.<>p__10 = CallSite<Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon>>.Create(Binder.InvokeMember(CSharpBinderFlags.ResultDiscarded, "Show", null, typeof(Form1), new CSharpArgumentInfo[]
									{
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.IsStaticType, null),
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null),
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null)
									}));
								}
								Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon> target3 = Form1.<>o__18.<>p__10.Target;
								CallSite <>p__3 = Form1.<>o__18.<>p__10;
								Type typeFromHandle2 = typeof(MessageBox);
								if (Form1.<>o__18.<>p__9 == null)
								{
									Form1.<>o__18.<>p__9 = CallSite<Func<CallSite, object, object>>.Create(Binder.InvokeMember(CSharpBinderFlags.None, "ToString", null, typeof(Form1), new CSharpArgumentInfo[]
									{
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
									}));
								}
								target3(<>p__3, typeFromHandle2, Form1.<>o__18.<>p__9.Target(Form1.<>o__18.<>p__9, arg), "DiagEx Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
								goto IL_DFC;
							}
						}
						else if (soapAction == "CloseAllJobs")
						{
							object arg = (from x in xdocument.Descendants()
							where x.Name.LocalName == "CloseAllJobsResult"
							select x).FirstOrDefault<XElement>();
							if (Form1.<>o__18.<>p__24 == null)
							{
								Form1.<>o__18.<>p__24 = CallSite<Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon>>.Create(Binder.InvokeMember(CSharpBinderFlags.ResultDiscarded, "Show", null, typeof(Form1), new CSharpArgumentInfo[]
								{
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.IsStaticType, null),
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null),
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null)
								}));
							}
							Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon> target4 = Form1.<>o__18.<>p__24.Target;
							CallSite <>p__4 = Form1.<>o__18.<>p__24;
							Type typeFromHandle3 = typeof(MessageBox);
							if (Form1.<>o__18.<>p__23 == null)
							{
								Form1.<>o__18.<>p__23 = CallSite<Func<CallSite, string, object, object>>.Create(Binder.BinaryOperation(CSharpBinderFlags.None, ExpressionType.Add, typeof(Form1), new CSharpArgumentInfo[]
								{
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
								}));
							}
							Func<CallSite, string, object, object> target5 = Form1.<>o__18.<>p__23.Target;
							CallSite <>p__5 = Form1.<>o__18.<>p__23;
							string arg2 = "Jobs closed: ";
							if (Form1.<>o__18.<>p__22 == null)
							{
								Form1.<>o__18.<>p__22 = CallSite<Func<CallSite, object, object>>.Create(Binder.InvokeMember(CSharpBinderFlags.None, "ToString", null, typeof(Form1), new CSharpArgumentInfo[]
								{
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
								}));
							}
							Func<CallSite, object, object> target6 = Form1.<>o__18.<>p__22.Target;
							CallSite <>p__6 = Form1.<>o__18.<>p__22;
							if (Form1.<>o__18.<>p__21 == null)
							{
								Form1.<>o__18.<>p__21 = CallSite<Func<CallSite, object, object>>.Create(Binder.GetMember(CSharpBinderFlags.None, "FirstNode", typeof(Form1), new CSharpArgumentInfo[]
								{
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
								}));
							}
							target4(<>p__4, typeFromHandle3, target5(<>p__5, arg2, target6(<>p__6, Form1.<>o__18.<>p__21.Target(Form1.<>o__18.<>p__21, arg))), "CloseAllJobs Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
							goto IL_DFC;
						}
					}
					else if (num <= 779408226U)
					{
						if (num != 650159416U)
						{
							if (num == 779408226U)
							{
								if (soapAction == "GetAllJobs")
								{
									object arg = (from x in xdocument.Descendants()
									where x.Name.LocalName == "GetAllJobsResult"
									select x).FirstOrDefault<XElement>();
									if (Form1.<>o__18.<>p__16 == null)
									{
										Form1.<>o__18.<>p__16 = CallSite<Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon>>.Create(Binder.InvokeMember(CSharpBinderFlags.ResultDiscarded, "Show", null, typeof(Form1), new CSharpArgumentInfo[]
										{
											CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.IsStaticType, null),
											CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null),
											CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
											CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
											CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null)
										}));
									}
									Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon> target7 = Form1.<>o__18.<>p__16.Target;
									CallSite <>p__7 = Form1.<>o__18.<>p__16;
									Type typeFromHandle4 = typeof(MessageBox);
									if (Form1.<>o__18.<>p__15 == null)
									{
										Form1.<>o__18.<>p__15 = CallSite<Func<CallSite, object, object>>.Create(Binder.InvokeMember(CSharpBinderFlags.None, "ToString", null, typeof(Form1), new CSharpArgumentInfo[]
										{
											CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
										}));
									}
									target7(<>p__7, typeFromHandle4, Form1.<>o__18.<>p__15.Target(Form1.<>o__18.<>p__15, arg), "GetAllJobs Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
									goto IL_DFC;
								}
							}
						}
						else if (soapAction == "Execute")
						{
							MessageBox.Show("Success!", "Execute Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
							goto IL_DFC;
						}
					}
					else if (num != 926844193U)
					{
						if (num == 976181145U)
						{
							if (soapAction == "GetVersion")
							{
								object arg = (from x in xdocument.Descendants()
								where x.Name.LocalName == "GetVersionResult"
								select x).FirstOrDefault<XElement>();
								if (Form1.<>o__18.<>p__5 == null)
								{
									Form1.<>o__18.<>p__5 = CallSite<Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon>>.Create(Binder.InvokeMember(CSharpBinderFlags.ResultDiscarded, "Show", null, typeof(Form1), new CSharpArgumentInfo[]
									{
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.IsStaticType, null),
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null),
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null)
									}));
								}
								Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon> target8 = Form1.<>o__18.<>p__5.Target;
								CallSite <>p__8 = Form1.<>o__18.<>p__5;
								Type typeFromHandle5 = typeof(MessageBox);
								if (Form1.<>o__18.<>p__4 == null)
								{
									Form1.<>o__18.<>p__4 = CallSite<Func<CallSite, object, object>>.Create(Binder.InvokeMember(CSharpBinderFlags.None, "ToString", null, typeof(Form1), new CSharpArgumentInfo[]
									{
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
									}));
								}
								Func<CallSite, object, object> target9 = Form1.<>o__18.<>p__4.Target;
								CallSite <>p__9 = Form1.<>o__18.<>p__4;
								if (Form1.<>o__18.<>p__3 == null)
								{
									Form1.<>o__18.<>p__3 = CallSite<Func<CallSite, object, object>>.Create(Binder.GetMember(CSharpBinderFlags.None, "FirstNode", typeof(Form1), new CSharpArgumentInfo[]
									{
										CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
									}));
								}
								target8(<>p__8, typeFromHandle5, target9(<>p__9, Form1.<>o__18.<>p__3.Target(Form1.<>o__18.<>p__3, arg)), "GetVersion Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
								goto IL_DFC;
							}
						}
					}
					else if (soapAction == "HelloWorld")
					{
						object arg = (from x in xdocument.Descendants()
						where x.Name.LocalName == "HelloWorldResult"
						select x).FirstOrDefault<XElement>();
						if (Form1.<>o__18.<>p__2 == null)
						{
							Form1.<>o__18.<>p__2 = CallSite<Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon>>.Create(Binder.InvokeMember(CSharpBinderFlags.ResultDiscarded, "Show", null, typeof(Form1), new CSharpArgumentInfo[]
							{
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.IsStaticType, null),
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null),
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null)
							}));
						}
						Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon> target10 = Form1.<>o__18.<>p__2.Target;
						CallSite <>p__10 = Form1.<>o__18.<>p__2;
						Type typeFromHandle6 = typeof(MessageBox);
						if (Form1.<>o__18.<>p__1 == null)
						{
							Form1.<>o__18.<>p__1 = CallSite<Func<CallSite, object, object>>.Create(Binder.InvokeMember(CSharpBinderFlags.None, "ToString", null, typeof(Form1), new CSharpArgumentInfo[]
							{
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
							}));
						}
						Func<CallSite, object, object> target11 = Form1.<>o__18.<>p__1.Target;
						CallSite <>p__11 = Form1.<>o__18.<>p__1;
						if (Form1.<>o__18.<>p__0 == null)
						{
							Form1.<>o__18.<>p__0 = CallSite<Func<CallSite, object, object>>.Create(Binder.GetMember(CSharpBinderFlags.None, "FirstNode", typeof(Form1), new CSharpArgumentInfo[]
							{
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
							}));
						}
						target10(<>p__10, typeFromHandle6, target11(<>p__11, Form1.<>o__18.<>p__0.Target(Form1.<>o__18.<>p__0, arg)), "HelloWorld Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
						goto IL_DFC;
					}
				}
				else if (num <= 2881278149U)
				{
					if (num != 2228970925U)
					{
						if (num != 2859263402U)
						{
							if (num == 2881278149U)
							{
								if (soapAction == "OpenJobEx")
								{
									MessageBox.Show("Success!", "OpenJobEx Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
									goto IL_DFC;
								}
							}
						}
						else if (soapAction == "CloseJob")
						{
							MessageBox.Show("Success!", "CloseJob Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
							goto IL_DFC;
						}
					}
					else if (soapAction == "ExecuteEx")
					{
						MessageBox.Show("Success!", "ExecuteEx Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
						goto IL_DFC;
					}
				}
				else if (num <= 3484949344U)
				{
					if (num != 3243501320U)
					{
						if (num == 3484949344U)
						{
							if (soapAction == "OpenJob")
							{
								goto IL_DFC;
							}
						}
					}
					else if (soapAction == "CloseExpiredJobs")
					{
						object arg = (from x in xdocument.Descendants()
						where x.Name.LocalName == "CloseExpiredJobsResult"
						select x).FirstOrDefault<XElement>();
						if (Form1.<>o__18.<>p__20 == null)
						{
							Form1.<>o__18.<>p__20 = CallSite<Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon>>.Create(Binder.InvokeMember(CSharpBinderFlags.ResultDiscarded, "Show", null, typeof(Form1), new CSharpArgumentInfo[]
							{
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.IsStaticType, null),
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null),
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null)
							}));
						}
						Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon> target12 = Form1.<>o__18.<>p__20.Target;
						CallSite <>p__12 = Form1.<>o__18.<>p__20;
						Type typeFromHandle7 = typeof(MessageBox);
						if (Form1.<>o__18.<>p__19 == null)
						{
							Form1.<>o__18.<>p__19 = CallSite<Func<CallSite, string, object, object>>.Create(Binder.BinaryOperation(CSharpBinderFlags.None, ExpressionType.Add, typeof(Form1), new CSharpArgumentInfo[]
							{
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
							}));
						}
						Func<CallSite, string, object, object> target13 = Form1.<>o__18.<>p__19.Target;
						CallSite <>p__13 = Form1.<>o__18.<>p__19;
						string arg3 = "Jobs closed: ";
						if (Form1.<>o__18.<>p__18 == null)
						{
							Form1.<>o__18.<>p__18 = CallSite<Func<CallSite, object, object>>.Create(Binder.InvokeMember(CSharpBinderFlags.None, "ToString", null, typeof(Form1), new CSharpArgumentInfo[]
							{
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
							}));
						}
						Func<CallSite, object, object> target14 = Form1.<>o__18.<>p__18.Target;
						CallSite <>p__14 = Form1.<>o__18.<>p__18;
						if (Form1.<>o__18.<>p__17 == null)
						{
							Form1.<>o__18.<>p__17 = CallSite<Func<CallSite, object, object>>.Create(Binder.GetMember(CSharpBinderFlags.None, "FirstNode", typeof(Form1), new CSharpArgumentInfo[]
							{
								CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
							}));
						}
						target12(<>p__12, typeFromHandle7, target13(<>p__13, arg3, target14(<>p__14, Form1.<>o__18.<>p__17.Target(Form1.<>o__18.<>p__17, arg))), "CloseExpiredJobs Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
						goto IL_DFC;
					}
				}
				else if (num != 3533170478U)
				{
					if (num == 3805855655U)
					{
						if (soapAction == "GetAllJobsEx")
						{
							object arg = (from x in xdocument.Descendants()
							where x.Name.LocalName == "GetAllJobsExResult"
							select x).FirstOrDefault<XElement>();
							if (Form1.<>o__18.<>p__14 == null)
							{
								Form1.<>o__18.<>p__14 = CallSite<Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon>>.Create(Binder.InvokeMember(CSharpBinderFlags.ResultDiscarded, "Show", null, typeof(Form1), new CSharpArgumentInfo[]
								{
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.IsStaticType, null),
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null),
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null)
								}));
							}
							Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon> target15 = Form1.<>o__18.<>p__14.Target;
							CallSite <>p__15 = Form1.<>o__18.<>p__14;
							Type typeFromHandle8 = typeof(MessageBox);
							if (Form1.<>o__18.<>p__13 == null)
							{
								Form1.<>o__18.<>p__13 = CallSite<Func<CallSite, object, object>>.Create(Binder.InvokeMember(CSharpBinderFlags.None, "ToString", null, typeof(Form1), new CSharpArgumentInfo[]
								{
									CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
								}));
							}
							target15(<>p__15, typeFromHandle8, Form1.<>o__18.<>p__13.Target(Form1.<>o__18.<>p__13, arg), "GetAllJobsEx Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
							goto IL_DFC;
						}
					}
				}
				else if (soapAction == "Diag")
				{
					object arg = (from x in xdocument.Descendants()
					where x.Name.LocalName == "DiagResult"
					select x).FirstOrDefault<XElement>();
					if (Form1.<>o__18.<>p__12 == null)
					{
						Form1.<>o__18.<>p__12 = CallSite<Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon>>.Create(Binder.InvokeMember(CSharpBinderFlags.ResultDiscarded, "Show", null, typeof(Form1), new CSharpArgumentInfo[]
						{
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.IsStaticType, null),
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null),
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null),
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null)
						}));
					}
					Action<CallSite, Type, object, string, MessageBoxButtons, MessageBoxIcon> target16 = Form1.<>o__18.<>p__12.Target;
					CallSite <>p__16 = Form1.<>o__18.<>p__12;
					Type typeFromHandle9 = typeof(MessageBox);
					if (Form1.<>o__18.<>p__11 == null)
					{
						Form1.<>o__18.<>p__11 = CallSite<Func<CallSite, object, object>>.Create(Binder.InvokeMember(CSharpBinderFlags.None, "ToString", null, typeof(Form1), new CSharpArgumentInfo[]
						{
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
						}));
					}
					target16(<>p__16, typeFromHandle9, Form1.<>o__18.<>p__11.Target(Form1.<>o__18.<>p__11, arg), "Diag Response", MessageBoxButtons.OK, MessageBoxIcon.Asterisk);
					goto IL_DFC;
				}
				MessageBox.Show("Attempt to call ParseXML(string xml, string soapAction) with invalid arguments", "ParseXML(string xml, string soapAction) error", MessageBoxButtons.OK, MessageBoxIcon.Hand);
				IL_DFC:;
			}
			catch
			{
			}
		}

		// Token: 0x06000083 RID: 131 RVA: 0x0000CEE8 File Offset: 0x0000B0E8
		[CompilerGenerated]
		private List<LuaValueNew> <timer1_Tick>g__GetLuaValues|18_2()
		{
			List<LuaValueNew> list = new List<LuaValueNew>();
			foreach (object obj in this.scriptArgumentPanel.Controls)
			{
				Control control = (Control)obj;
				if (control.Name == "argumentTemplate" && control.Visible)
				{
					list.Add(new LuaValueNew(control.Controls["argumentType"].Text, control.Controls["argumentValue"].Text));
				}
			}
			return list;
		}

		// Token: 0x06000084 RID: 132 RVA: 0x0000CF98 File Offset: 0x0000B198
		[CompilerGenerated]
		internal static string <timer1_Tick>g__SendRequestToGameServer|18_3(int servicePort, string action, string content, string url, string ip)
		{
			string result;
			using (WebClient webClient = new WebClient())
			{
				try
				{
					string data = Form1.<timer1_Tick>g__GenerateContentXML|18_0(url, content);
					webClient.Encoding = Encoding.UTF8;
					webClient.Headers.Add("Accept", "text/xml");
					webClient.Headers.Add("Cache-Control", "no-cache");
					webClient.Headers.Add("Pragma", "no-cache");
					webClient.Headers.Add("SOAPAction", action);
					string text = webClient.UploadString("http://" + ip + ":" + servicePort.ToString(), data);
					MessageBox.Show(text);
					result = text;
				}
				catch
				{
					result = "";
				}
			}
			return result;
		}

		// Token: 0x06000085 RID: 133 RVA: 0x0000D068 File Offset: 0x0000B268
		[CompilerGenerated]
		internal static string <timer1_Tick>g__ParseArguments|18_4(List<LuaValueNew> args)
		{
			if (args != null)
			{
				string text = "";
				foreach (LuaValueNew luaValueNew in args)
				{
					if (Form1.<>o__18.<>p__28 == null)
					{
						Form1.<>o__18.<>p__28 = CallSite<Func<CallSite, object, string>>.Create(Binder.Convert(CSharpBinderFlags.ConvertExplicit, typeof(string), typeof(Form1)));
					}
					Func<CallSite, object, string> target = Form1.<>o__18.<>p__28.Target;
					CallSite <>p__ = Form1.<>o__18.<>p__28;
					if (Form1.<>o__18.<>p__27 == null)
					{
						Form1.<>o__18.<>p__27 = CallSite<Func<CallSite, string, object, object>>.Create(Binder.BinaryOperation(CSharpBinderFlags.None, ExpressionType.AddAssign, typeof(Form1), new CSharpArgumentInfo[]
						{
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType, null),
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
						}));
					}
					Func<CallSite, string, object, object> target2 = Form1.<>o__18.<>p__27.Target;
					CallSite <>p__2 = Form1.<>o__18.<>p__27;
					string arg = text;
					if (Form1.<>o__18.<>p__26 == null)
					{
						Form1.<>o__18.<>p__26 = CallSite<Func<CallSite, object, string, object>>.Create(Binder.BinaryOperation(CSharpBinderFlags.None, ExpressionType.Add, typeof(Form1), new CSharpArgumentInfo[]
						{
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null),
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType | CSharpArgumentInfoFlags.Constant, null)
						}));
					}
					Func<CallSite, object, string, object> target3 = Form1.<>o__18.<>p__26.Target;
					CallSite <>p__3 = Form1.<>o__18.<>p__26;
					if (Form1.<>o__18.<>p__25 == null)
					{
						Form1.<>o__18.<>p__25 = CallSite<Func<CallSite, string, object, object>>.Create(Binder.BinaryOperation(CSharpBinderFlags.None, ExpressionType.Add, typeof(Form1), new CSharpArgumentInfo[]
						{
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.UseCompileTimeType, null),
							CSharpArgumentInfo.Create(CSharpArgumentInfoFlags.None, null)
						}));
					}
					text = target(<>p__, target2(<>p__2, arg, target3(<>p__3, Form1.<>o__18.<>p__25.Target(Form1.<>o__18.<>p__25, "<ns1:LuaValue><ns1:type>" + luaValueNew.type + "</ns1:type><ns1:value>", luaValueNew.value), "</ns1:value></ns1:LuaValue>")));
				}
				return text;
			}
			return "";
		}

		// Token: 0x0400001E RID: 30
		private string http = "http";

		// Token: 0x0400001F RID: 31
		private int num;

		// Token: 0x04000020 RID: 32
		private string assetsaving = "true";

		// Token: 0x04000021 RID: 33
		private string headcolor = "Pastel brown";

		// Token: 0x04000022 RID: 34
		private string torsocolor = "Pastel brown";

		// Token: 0x04000023 RID: 35
		private string leftlegcolor = "Pastel brown";

		// Token: 0x04000024 RID: 36
		private string rightlegcolor = "Pastel brown";

		// Token: 0x04000025 RID: 37
		private string leftarmcolor = "Pastel brown";

		// Token: 0x04000026 RID: 38
		private string rightarmcolor = "Pastel brown";

		// Token: 0x04000027 RID: 39
		private string chartype = "R6";

		// Token: 0x04000028 RID: 40
		private bool started2017 = true;

		// Token: 0x04000029 RID: 41
		private bool started2008 = true;

		// Token: 0x0400002A RID: 42
		private Point startPoint = new Point(0, 0);

		// Token: 0x0400002B RID: 43
		private System.Windows.Forms.Timer timer1;

		// Token: 0x0400002C RID: 44
		private string selectedbodypart = "Head";

		// Token: 0x0400002D RID: 45
		private string currentclient = "2018M";

		// Token: 0x0400002E RID: 46
		private static readonly Regex sWhitespace = new Regex("\\s+");

		// Token: 0x0400002F RID: 47
		private bool _dragging;

		// Token: 0x04000030 RID: 48
		private Point _start_point = new Point(0, 0);
	}
}
