using System;
using System.Diagnostics;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;

namespace Restaurante;

class Program
{
    static async Task Main(string[] args)
    {
        // 1. Cargar la configuración usando tu método existente
        var configuration = BuildConfiguration();

        // 2. Instanciar el Productor e inicializar su conexión de forma asíncrona
        var producer = await Producer.CreateAsync(configuration);

        Console.WriteLine("=== SISTEMA RESTAURANTE (PRODUCTOR) ===");
        Console.WriteLine("Introduce el nombre del pedido (escribe 'salir' para terminar):");

        // 3. Bucle para solicitar pedidos de forma recurrente
        while (true)
        {
            Console.Write("\nNuevo pedido: ");
            var pedido = Console.ReadLine();

            if (string.IsNullOrWhiteSpace(pedido) || pedido.Equals("salir", StringComparison.OrdinalIgnoreCase))
            {
                break;
            }

            // 4. Enviar el mensaje a la cola
            bool exito = await producer.SendMessage(pedido);

            // 5. Mostrar mensaje por consola indicando éxito o fracaso
            if (exito)
            {
                Console.WriteLine("-> [ÉXITO] El mensaje se ha enviado correctamente a la cola.");
            }
            else
            {
                Console.WriteLine("-> [ERROR] No se pudo enviar el mensaje a la cola.");
            }
        }
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
