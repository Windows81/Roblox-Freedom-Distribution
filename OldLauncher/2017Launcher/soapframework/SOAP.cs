using System;
using System.Collections.Generic;
using System.Net;

namespace soapframework
{
	// Token: 0x02000002 RID: 2
	public class SOAP
	{
		// Token: 0x06000001 RID: 1 RVA: 0x00002050 File Offset: 0x00000250
		private static string post(string content, string action, string service, string baseurl, string http)
		{
			Dictionary<string, string> dictionary = new Dictionary<string, string>
			{
				{
					"Accept",
					"text/xml"
				},
				{
					"Cache-Control",
					"no-cache"
				},
				{
					"Pragma",
					"no-cache"
				},
				{
					"SOAPAction",
					action
				}
			};
			content = string.Concat(new string[]
			{
				"<?xml version=\"1.0\" encoding=\"UTF - 8\"?>\r\n<SOAP-ENV:Envelope xmlns:SOAP-ENV=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:SOAP-ENC=\"http://schemas.xmlsoap.org/soap/encoding/\" xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xmlns:xsd=\"http://www.w3.org/2001/XMLSchema\" xmlns:ns2=\"",
				http,
				"://",
				baseurl,
				"/RCCServiceSoap\" xmlns:ns1=\"",
				http,
				"://",
				baseurl,
				"/\" xmlns:ns3=\"",
				http,
				"://",
				baseurl,
				"/RCCServiceSoap12\">\r\n\t<SOAP-ENV:Body>",
				content,
				"\t</SOAP-ENV:Body>\r\n</SOAP-ENV:Envelope>"
			});
			string result;
			using (WebClient webClient = new WebClient())
			{
				foreach (KeyValuePair<string, string> keyValuePair in dictionary)
				{
					webClient.Headers.Add(keyValuePair.Key, keyValuePair.Value);
				}
				try
				{
					result = webClient.UploadString("http://" + service, content);
				}
				catch (Exception ex)
				{
					result = ex.ToString();
				}
			}
			return result;
		}

		// Token: 0x06000002 RID: 2 RVA: 0x000021B0 File Offset: 0x000003B0
		public static void ExecuteScript(string service, string scriptName, string baseScript, string JobId, string args, string baseurl, string http)
		{
			SOAP.post(string.Concat(new string[]
			{
				"\t\t<ns1:Execute>\r\n\t\t\t<ns1:jobID>",
				JobId,
				"</ns1:jobID>\r\n\t\t\t<ns1:script>\r\n\t\t\t\t<ns1:name>",
				scriptName,
				"</ns1:name>\r\n\t\t\t\t<ns1:script>",
				baseScript,
				"</ns1:script>\r\n\t\t\t\t<ns1:arguments>",
				SOAP.argumentParser(args),
				"\r\n\t\t\t\t</ns1:arguments>\r\n\t\t\t</ns1:script>\r\n\t\t</ns1:Execute>"
			}), "Execute", service, baseurl, http);
		}

		// Token: 0x06000003 RID: 3 RVA: 0x00002218 File Offset: 0x00000418
		private static string GenerateUUIDV4()
		{
			return Guid.NewGuid().ToString();
		}

		// Token: 0x06000004 RID: 4 RVA: 0x00002238 File Offset: 0x00000438
		public static void jsonExecute(string baseurl, string service, string baseScript, string http)
		{
			SOAP.post("\r\n<ns1:OpenJob>\r\n<ns1:job>\r\n\t<ns1:expirationInSeconds>999999999999</ns1:expirationInSeconds>\r\n\t<ns1:id>Test</ns1:id>\r\n\t</ns1:job>\r\n\t<ns1:script>\r\n\t\t<ns1:name>Test</ns1:name>\r\n\t\t<ns1:script>" + baseScript + "</ns1:script>\r\n\t<ns1:arguments>Not Implemented\r\n\t\t\t\t</ns1:arguments>\r\n\t</ns1:script>\r\n</ns1:BatchJob>\r\n", "OpenJob", service + "/OpenJob", baseurl, http);
		}

		// Token: 0x06000005 RID: 5 RVA: 0x00002262 File Offset: 0x00000462
		private static string argumentParser(string args)
		{
			return "Not Implemented";
		}
	}
}
