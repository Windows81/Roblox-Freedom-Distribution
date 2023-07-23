namespace _2017Launcher
{
	// Token: 0x02000003 RID: 3
	public partial class Form1 : global::System.Windows.Forms.Form
	{
		// Token: 0x06000027 RID: 39 RVA: 0x0000435B File Offset: 0x0000255B
		protected override void Dispose(bool disposing)
		{
			if (disposing && this.components != null)
			{
				this.components.Dispose();
			}
			base.Dispose(disposing);
		}

		// Token: 0x06000028 RID: 40 RVA: 0x0000437C File Offset: 0x0000257C
		private void InitializeComponent()
		{
			this.button1 = new global::System.Windows.Forms.Button();
			this.label2 = new global::System.Windows.Forms.Label();
			this.button2 = new global::System.Windows.Forms.Button();
			this.textBox2 = new global::System.Windows.Forms.TextBox();
			this.label3 = new global::System.Windows.Forms.Label();
			this.textBox3 = new global::System.Windows.Forms.TextBox();
			this.label1 = new global::System.Windows.Forms.Label();
			this.textBox1 = new global::System.Windows.Forms.TextBox();
			this.button3 = new global::System.Windows.Forms.Button();
			this.listBox1 = new global::System.Windows.Forms.ListBox();
			this.textBox4 = new global::System.Windows.Forms.TextBox();
			this.label4 = new global::System.Windows.Forms.Label();
			this.label5 = new global::System.Windows.Forms.Label();
			this.tabControl1 = new global::System.Windows.Forms.TabControl();
			this.tabPage1 = new global::System.Windows.Forms.TabPage();
			this.tabPage2 = new global::System.Windows.Forms.TabPage();
			this.tabPage3 = new global::System.Windows.Forms.TabPage();
			this.label9 = new global::System.Windows.Forms.Label();
			this.label8 = new global::System.Windows.Forms.Label();
			this.label7 = new global::System.Windows.Forms.Label();
			this.label6 = new global::System.Windows.Forms.Label();
			this.tabPage4 = new global::System.Windows.Forms.TabPage();
			this.pictureBox10 = new global::System.Windows.Forms.PictureBox();
			this.pictureBox9 = new global::System.Windows.Forms.PictureBox();
			this.pictureBox7 = new global::System.Windows.Forms.PictureBox();
			this.pictureBox8 = new global::System.Windows.Forms.PictureBox();
			this.pictureBox6 = new global::System.Windows.Forms.PictureBox();
			this.pictureBox5 = new global::System.Windows.Forms.PictureBox();
			this.pictureBox4 = new global::System.Windows.Forms.PictureBox();
			this.pictureBox3 = new global::System.Windows.Forms.PictureBox();
			this.pictureBox2 = new global::System.Windows.Forms.PictureBox();
			this.pictureBox1 = new global::System.Windows.Forms.PictureBox();
			this.label10 = new global::System.Windows.Forms.Label();
			this.colorDialog1 = new global::System.Windows.Forms.ColorDialog();
			this.button4 = new global::System.Windows.Forms.Button();
			this.button5 = new global::System.Windows.Forms.Button();
			this.tabControl1.SuspendLayout();
			this.tabPage1.SuspendLayout();
			this.tabPage2.SuspendLayout();
			this.tabPage3.SuspendLayout();
			this.tabPage4.SuspendLayout();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox10).BeginInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox9).BeginInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox7).BeginInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox8).BeginInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox6).BeginInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox5).BeginInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox4).BeginInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox3).BeginInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox2).BeginInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox1).BeginInit();
			base.SuspendLayout();
			this.button1.Location = new global::System.Drawing.Point(57, 78);
			this.button1.Name = "button1";
			this.button1.Size = new global::System.Drawing.Size(145, 27);
			this.button1.TabIndex = 0;
			this.button1.Text = "Host";
			this.button1.UseVisualStyleBackColor = true;
			this.button1.Click += new global::System.EventHandler(this.button1_Click);
			this.label2.AutoSize = true;
			this.label2.Location = new global::System.Drawing.Point(83, 44);
			this.label2.Name = "label2";
			this.label2.Size = new global::System.Drawing.Size(26, 13);
			this.label2.TabIndex = 3;
			this.label2.Text = "Port";
			this.button2.Location = new global::System.Drawing.Point(80, 124);
			this.button2.Name = "button2";
			this.button2.Size = new global::System.Drawing.Size(100, 23);
			this.button2.TabIndex = 4;
			this.button2.Text = "Join";
			this.button2.UseVisualStyleBackColor = true;
			this.button2.Click += new global::System.EventHandler(this.button2_Click);
			this.textBox2.Location = new global::System.Drawing.Point(80, 60);
			this.textBox2.Name = "textBox2";
			this.textBox2.Size = new global::System.Drawing.Size(100, 20);
			this.textBox2.TabIndex = 5;
			this.textBox2.TextChanged += new global::System.EventHandler(this.textBox2_TextChanged);
			this.label3.AutoSize = true;
			this.label3.Location = new global::System.Drawing.Point(83, 6);
			this.label3.Name = "label3";
			this.label3.Size = new global::System.Drawing.Size(16, 13);
			this.label3.TabIndex = 6;
			this.label3.Text = "Ip";
			this.textBox3.Location = new global::System.Drawing.Point(80, 22);
			this.textBox3.Name = "textBox3";
			this.textBox3.Size = new global::System.Drawing.Size(100, 20);
			this.textBox3.TabIndex = 7;
			this.label1.AutoSize = true;
			this.label1.Location = new global::System.Drawing.Point(83, 83);
			this.label1.Name = "label1";
			this.label1.Size = new global::System.Drawing.Size(55, 13);
			this.label1.TabIndex = 8;
			this.label1.Text = "Username";
			this.textBox1.Location = new global::System.Drawing.Point(80, 98);
			this.textBox1.Name = "textBox1";
			this.textBox1.Size = new global::System.Drawing.Size(100, 20);
			this.textBox1.TabIndex = 9;
			this.textBox1.TextChanged += new global::System.EventHandler(this.textBox1_TextChanged);
			this.button3.Location = new global::System.Drawing.Point(57, 47);
			this.button3.Name = "button3";
			this.button3.Size = new global::System.Drawing.Size(145, 28);
			this.button3.TabIndex = 10;
			this.button3.Text = "Choose map";
			this.button3.UseVisualStyleBackColor = true;
			this.button3.Click += new global::System.EventHandler(this.button3_Click);
			this.listBox1.BackColor = global::System.Drawing.Color.FromArgb(70, 15, 64);
			this.listBox1.ForeColor = global::System.Drawing.SystemColors.Info;
			this.listBox1.FormattingEnabled = true;
			this.listBox1.Items.AddRange(new object[]
			{
				"Empty"
			});
			this.listBox1.Location = new global::System.Drawing.Point(285, 15);
			this.listBox1.Name = "listBox1";
			this.listBox1.Size = new global::System.Drawing.Size(132, 186);
			this.listBox1.TabIndex = 24;
			this.listBox1.SelectedIndexChanged += new global::System.EventHandler(this.listBox1_SelectedIndexChanged);
			this.textBox4.Location = new global::System.Drawing.Point(57, 21);
			this.textBox4.Name = "textBox4";
			this.textBox4.Size = new global::System.Drawing.Size(145, 20);
			this.textBox4.TabIndex = 25;
			this.label4.AutoSize = true;
			this.label4.Location = new global::System.Drawing.Point(54, 5);
			this.label4.Name = "label4";
			this.label4.Size = new global::System.Drawing.Size(26, 13);
			this.label4.TabIndex = 26;
			this.label4.Text = "Port";
			this.label5.AutoSize = true;
			this.label5.Location = new global::System.Drawing.Point(282, -1);
			this.label5.Name = "label5";
			this.label5.Size = new global::System.Drawing.Size(38, 13);
			this.label5.TabIndex = 27;
			this.label5.Text = "Clients";
			this.tabControl1.Controls.Add(this.tabPage1);
			this.tabControl1.Controls.Add(this.tabPage2);
			this.tabControl1.Controls.Add(this.tabPage3);
			this.tabControl1.Controls.Add(this.tabPage4);
			this.tabControl1.Location = new global::System.Drawing.Point(1, -1);
			this.tabControl1.Name = "tabControl1";
			this.tabControl1.SelectedIndex = 0;
			this.tabControl1.Size = new global::System.Drawing.Size(278, 178);
			this.tabControl1.TabIndex = 30;
			this.tabPage1.Controls.Add(this.textBox3);
			this.tabPage1.Controls.Add(this.label3);
			this.tabPage1.Controls.Add(this.label2);
			this.tabPage1.Controls.Add(this.textBox2);
			this.tabPage1.Controls.Add(this.label1);
			this.tabPage1.Controls.Add(this.textBox1);
			this.tabPage1.Controls.Add(this.button2);
			this.tabPage1.Location = new global::System.Drawing.Point(4, 22);
			this.tabPage1.Name = "tabPage1";
			this.tabPage1.Padding = new global::System.Windows.Forms.Padding(3);
			this.tabPage1.Size = new global::System.Drawing.Size(270, 152);
			this.tabPage1.TabIndex = 0;
			this.tabPage1.Text = "Play";
			this.tabPage1.UseVisualStyleBackColor = true;
			this.tabPage2.Controls.Add(this.label4);
			this.tabPage2.Controls.Add(this.textBox4);
			this.tabPage2.Controls.Add(this.button3);
			this.tabPage2.Controls.Add(this.button1);
			this.tabPage2.Location = new global::System.Drawing.Point(4, 22);
			this.tabPage2.Name = "tabPage2";
			this.tabPage2.Padding = new global::System.Windows.Forms.Padding(3);
			this.tabPage2.Size = new global::System.Drawing.Size(270, 152);
			this.tabPage2.TabIndex = 1;
			this.tabPage2.Text = "Host";
			this.tabPage2.UseVisualStyleBackColor = true;
			this.tabPage3.Controls.Add(this.label9);
			this.tabPage3.Controls.Add(this.label8);
			this.tabPage3.Controls.Add(this.label7);
			this.tabPage3.Controls.Add(this.label6);
			this.tabPage3.Location = new global::System.Drawing.Point(4, 22);
			this.tabPage3.Name = "tabPage3";
			this.tabPage3.Size = new global::System.Drawing.Size(270, 152);
			this.tabPage3.TabIndex = 2;
			this.tabPage3.Text = "Credits";
			this.tabPage3.UseVisualStyleBackColor = true;
			this.label9.AutoSize = true;
			this.label9.Location = new global::System.Drawing.Point(3, 120);
			this.label9.Name = "label9";
			this.label9.Size = new global::System.Drawing.Size(177, 26);
			this.label9.TabIndex = 3;
			this.label9.Text = "\ud835\udd4e\ud835\udd5a\ud835\udd5f\ud835\udd55\ud835\udd60\ud835\udd68\ud835\udd64 \ud835\udfdf#8789 Making eclipse, \r\ngiving ideas for the launcher.";
			this.label8.AutoSize = true;
			this.label8.Location = new global::System.Drawing.Point(3, 71);
			this.label8.Name = "label8";
			this.label8.Size = new global::System.Drawing.Size(202, 39);
			this.label8.TabIndex = 2;
			this.label8.Text = "iknowidontexistbutwhatifwin \r\nGreat guy, helped patch 2022 studio.\r\n(He left the ORC so please dont DM him.)";
			this.label7.AutoSize = true;
			this.label7.Location = new global::System.Drawing.Point(3, 0);
			this.label7.Name = "label7";
			this.label7.Size = new global::System.Drawing.Size(222, 26);
			this.label7.TabIndex = 1;
			this.label7.Text = "[Σ]filibuster#3323, Helping patch features I\r\n couldn't like tickets, and various other things.";
			this.label6.AutoSize = true;
			this.label6.Location = new global::System.Drawing.Point(3, 35);
			this.label6.Name = "label6";
			this.label6.Size = new global::System.Drawing.Size(206, 26);
			this.label6.TabIndex = 0;
			this.label6.Text = "Jetray#4509, helping patch clients,\r\n building the launcher, and doing charapp.";
			this.tabPage4.Controls.Add(this.pictureBox10);
			this.tabPage4.Controls.Add(this.pictureBox9);
			this.tabPage4.Controls.Add(this.pictureBox7);
			this.tabPage4.Controls.Add(this.pictureBox8);
			this.tabPage4.Controls.Add(this.pictureBox6);
			this.tabPage4.Controls.Add(this.pictureBox5);
			this.tabPage4.Controls.Add(this.pictureBox4);
			this.tabPage4.Controls.Add(this.pictureBox3);
			this.tabPage4.Controls.Add(this.pictureBox2);
			this.tabPage4.Controls.Add(this.pictureBox1);
			this.tabPage4.Controls.Add(this.label10);
			this.tabPage4.Location = new global::System.Drawing.Point(4, 22);
			this.tabPage4.Name = "tabPage4";
			this.tabPage4.Padding = new global::System.Windows.Forms.Padding(3);
			this.tabPage4.Size = new global::System.Drawing.Size(270, 152);
			this.tabPage4.TabIndex = 3;
			this.tabPage4.Text = "Settings";
			this.tabPage4.UseVisualStyleBackColor = true;
			this.pictureBox10.BackColor = global::System.Drawing.Color.Goldenrod;
			this.pictureBox10.Location = new global::System.Drawing.Point(183, 112);
			this.pictureBox10.Name = "pictureBox10";
			this.pictureBox10.Size = new global::System.Drawing.Size(19, 34);
			this.pictureBox10.TabIndex = 12;
			this.pictureBox10.TabStop = false;
			this.pictureBox10.Click += new global::System.EventHandler(this.pictureBox10_Click);
			this.pictureBox9.BackColor = global::System.Drawing.Color.Goldenrod;
			this.pictureBox9.Location = new global::System.Drawing.Point(159, 112);
			this.pictureBox9.Name = "pictureBox9";
			this.pictureBox9.Size = new global::System.Drawing.Size(19, 34);
			this.pictureBox9.TabIndex = 11;
			this.pictureBox9.TabStop = false;
			this.pictureBox9.Click += new global::System.EventHandler(this.pictureBox9_Click);
			this.pictureBox7.BackColor = global::System.Drawing.Color.Goldenrod;
			this.pictureBox7.Location = new global::System.Drawing.Point(134, 48);
			this.pictureBox7.Name = "pictureBox7";
			this.pictureBox7.Size = new global::System.Drawing.Size(19, 57);
			this.pictureBox7.TabIndex = 10;
			this.pictureBox7.TabStop = false;
			this.pictureBox7.Click += new global::System.EventHandler(this.pictureBox7_Click);
			this.pictureBox8.BackColor = global::System.Drawing.Color.Goldenrod;
			this.pictureBox8.Location = new global::System.Drawing.Point(208, 48);
			this.pictureBox8.Name = "pictureBox8";
			this.pictureBox8.Size = new global::System.Drawing.Size(19, 57);
			this.pictureBox8.TabIndex = 9;
			this.pictureBox8.TabStop = false;
			this.pictureBox8.Click += new global::System.EventHandler(this.pictureBox8_Click);
			this.pictureBox6.BackColor = global::System.Drawing.Color.Goldenrod;
			this.pictureBox6.Location = new global::System.Drawing.Point(159, 49);
			this.pictureBox6.Name = "pictureBox6";
			this.pictureBox6.Size = new global::System.Drawing.Size(43, 57);
			this.pictureBox6.TabIndex = 7;
			this.pictureBox6.TabStop = false;
			this.pictureBox6.Click += new global::System.EventHandler(this.pictureBox6_Click);
			this.pictureBox5.BackColor = global::System.Drawing.Color.Goldenrod;
			this.pictureBox5.Location = new global::System.Drawing.Point(159, 6);
			this.pictureBox5.Name = "pictureBox5";
			this.pictureBox5.Size = new global::System.Drawing.Size(43, 37);
			this.pictureBox5.TabIndex = 6;
			this.pictureBox5.TabStop = false;
			this.pictureBox5.Click += new global::System.EventHandler(this.pictureBox5_Click);
			this.pictureBox4.BackColor = global::System.Drawing.Color.FromArgb(255, 170, 127);
			this.pictureBox4.Location = new global::System.Drawing.Point(93, 19);
			this.pictureBox4.Name = "pictureBox4";
			this.pictureBox4.Size = new global::System.Drawing.Size(22, 21);
			this.pictureBox4.TabIndex = 5;
			this.pictureBox4.TabStop = false;
			this.pictureBox4.Click += new global::System.EventHandler(this.pictureBox4_Click);
			this.pictureBox3.BackColor = global::System.Drawing.Color.DarkGoldenrod;
			this.pictureBox3.Location = new global::System.Drawing.Point(65, 19);
			this.pictureBox3.Name = "pictureBox3";
			this.pictureBox3.Size = new global::System.Drawing.Size(22, 21);
			this.pictureBox3.TabIndex = 4;
			this.pictureBox3.TabStop = false;
			this.pictureBox3.Click += new global::System.EventHandler(this.pictureBox3_Click);
			this.pictureBox2.BackColor = global::System.Drawing.Color.Goldenrod;
			this.pictureBox2.Location = new global::System.Drawing.Point(37, 19);
			this.pictureBox2.Name = "pictureBox2";
			this.pictureBox2.Size = new global::System.Drawing.Size(22, 21);
			this.pictureBox2.TabIndex = 3;
			this.pictureBox2.TabStop = false;
			this.pictureBox2.Click += new global::System.EventHandler(this.pictureBox2_Click);
			this.pictureBox1.BackColor = global::System.Drawing.Color.DeepSkyBlue;
			this.pictureBox1.Location = new global::System.Drawing.Point(10, 19);
			this.pictureBox1.Name = "pictureBox1";
			this.pictureBox1.Size = new global::System.Drawing.Size(22, 21);
			this.pictureBox1.TabIndex = 1;
			this.pictureBox1.TabStop = false;
			this.pictureBox1.Click += new global::System.EventHandler(this.pictureBox1_Click);
			this.label10.AutoSize = true;
			this.label10.Location = new global::System.Drawing.Point(17, 3);
			this.label10.Name = "label10";
			this.label10.Size = new global::System.Drawing.Size(55, 13);
			this.label10.TabIndex = 0;
			this.label10.Text = "BodyColor";
			this.button4.Location = new global::System.Drawing.Point(5, 178);
			this.button4.Name = "button4";
			this.button4.Size = new global::System.Drawing.Size(121, 23);
			this.button4.TabIndex = 31;
			this.button4.Text = "Start php server";
			this.button4.UseVisualStyleBackColor = true;
			this.button4.Click += new global::System.EventHandler(this.button4_Click);
			this.button5.Location = new global::System.Drawing.Point(132, 178);
			this.button5.Name = "button5";
			this.button5.Size = new global::System.Drawing.Size(121, 23);
			this.button5.TabIndex = 32;
			this.button5.Text = "Kill php server";
			this.button5.UseVisualStyleBackColor = true;
			this.button5.Click += new global::System.EventHandler(this.button5_Click);
			base.AutoScaleDimensions = new global::System.Drawing.SizeF(6f, 13f);
			base.AutoScaleMode = global::System.Windows.Forms.AutoScaleMode.Font;
			base.ClientSize = new global::System.Drawing.Size(420, 203);
			base.Controls.Add(this.button5);
			base.Controls.Add(this.button4);
			base.Controls.Add(this.tabControl1);
			base.Controls.Add(this.label5);
			base.Controls.Add(this.listBox1);
			this.MaximumSize = new global::System.Drawing.Size(436, 242);
			this.MinimumSize = new global::System.Drawing.Size(436, 242);
			base.Name = "Form1";
			this.Text = "Roblox Launcher";
			base.FormClosing += new global::System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
			base.FormClosed += new global::System.Windows.Forms.FormClosedEventHandler(this.Form1_FormClosed);
			base.Load += new global::System.EventHandler(this.Form1_Load);
			base.Shown += new global::System.EventHandler(this.Form1_Shown);
			this.tabControl1.ResumeLayout(false);
			this.tabPage1.ResumeLayout(false);
			this.tabPage1.PerformLayout();
			this.tabPage2.ResumeLayout(false);
			this.tabPage2.PerformLayout();
			this.tabPage3.ResumeLayout(false);
			this.tabPage3.PerformLayout();
			this.tabPage4.ResumeLayout(false);
			this.tabPage4.PerformLayout();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox10).EndInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox9).EndInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox7).EndInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox8).EndInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox6).EndInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox5).EndInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox4).EndInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox3).EndInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox2).EndInit();
			((global::System.ComponentModel.ISupportInitialize)this.pictureBox1).EndInit();
			base.ResumeLayout(false);
			base.PerformLayout();
		}

		// Token: 0x0400000E RID: 14
		private global::System.ComponentModel.IContainer components;

		// Token: 0x0400000F RID: 15
		private global::System.Windows.Forms.Button button1;

		// Token: 0x04000010 RID: 16
		private global::System.Windows.Forms.Label label2;

		// Token: 0x04000011 RID: 17
		private global::System.Windows.Forms.Button button2;

		// Token: 0x04000012 RID: 18
		private global::System.Windows.Forms.TextBox textBox2;

		// Token: 0x04000013 RID: 19
		private global::System.Windows.Forms.Label label3;

		// Token: 0x04000014 RID: 20
		private global::System.Windows.Forms.TextBox textBox3;

		// Token: 0x04000015 RID: 21
		private global::System.Windows.Forms.Label label1;

		// Token: 0x04000016 RID: 22
		private global::System.Windows.Forms.TextBox textBox1;

		// Token: 0x04000017 RID: 23
		private global::System.Windows.Forms.Button button3;

		// Token: 0x04000018 RID: 24
		private global::System.Windows.Forms.ListBox listBox1;

		// Token: 0x04000019 RID: 25
		private global::System.Windows.Forms.TextBox textBox4;

		// Token: 0x0400001A RID: 26
		private global::System.Windows.Forms.Label label4;

		// Token: 0x0400001B RID: 27
		private global::System.Windows.Forms.Label label5;

		// Token: 0x0400001C RID: 28
		private global::System.Windows.Forms.TabControl tabControl1;

		// Token: 0x0400001D RID: 29
		private global::System.Windows.Forms.TabPage tabPage1;

		// Token: 0x0400001E RID: 30
		private global::System.Windows.Forms.TabPage tabPage2;

		// Token: 0x0400001F RID: 31
		private global::System.Windows.Forms.TabPage tabPage3;

		// Token: 0x04000020 RID: 32
		private global::System.Windows.Forms.Label label9;

		// Token: 0x04000021 RID: 33
		private global::System.Windows.Forms.Label label8;

		// Token: 0x04000022 RID: 34
		private global::System.Windows.Forms.Label label7;

		// Token: 0x04000023 RID: 35
		private global::System.Windows.Forms.Label label6;

		// Token: 0x04000024 RID: 36
		private global::System.Windows.Forms.TabPage tabPage4;

		// Token: 0x04000025 RID: 37
		private global::System.Windows.Forms.PictureBox pictureBox1;

		// Token: 0x04000026 RID: 38
		private global::System.Windows.Forms.Label label10;

		// Token: 0x04000027 RID: 39
		private global::System.Windows.Forms.ColorDialog colorDialog1;

		// Token: 0x04000028 RID: 40
		private global::System.Windows.Forms.PictureBox pictureBox2;

		// Token: 0x04000029 RID: 41
		private global::System.Windows.Forms.PictureBox pictureBox3;

		// Token: 0x0400002A RID: 42
		private global::System.Windows.Forms.PictureBox pictureBox4;

		// Token: 0x0400002B RID: 43
		private global::System.Windows.Forms.Button button4;

		// Token: 0x0400002C RID: 44
		private global::System.Windows.Forms.Button button5;

		// Token: 0x0400002D RID: 45
		private global::System.Windows.Forms.PictureBox pictureBox10;

		// Token: 0x0400002E RID: 46
		private global::System.Windows.Forms.PictureBox pictureBox9;

		// Token: 0x0400002F RID: 47
		private global::System.Windows.Forms.PictureBox pictureBox7;

		// Token: 0x04000030 RID: 48
		private global::System.Windows.Forms.PictureBox pictureBox8;

		// Token: 0x04000031 RID: 49
		private global::System.Windows.Forms.PictureBox pictureBox6;

		// Token: 0x04000032 RID: 50
		private global::System.Windows.Forms.PictureBox pictureBox5;
	}
}
