
using System.Diagnostics;
using Microsoft.Extensions.Configuration;

namespace Restaurante;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Hello, World!");
    }

    private static IConfiguration BuildConfiguration()
    {
        var configurationBuilder = new ConfigurationBuilder()
            .SetBasePath(AppContext.BaseDirectory)
            .AddJsonFile("appsettings.json", optional: false);

        if (Debugger.IsAttached)
        {
            configurationBuilder.AddJsonFile(
                "appsettings.Development.json",
                optional: true
            );
        }

        return configurationBuilder.Build();
    }

    

    
}
