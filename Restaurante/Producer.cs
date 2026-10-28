using System; 
using System.Text;
using System.Threading.Tasks;
using Microsoft.Extensions.Configuration;
using RabbitMQ.Client; 

class Producer
{
    private readonly IConfiguration _configuration; 
    private readonly string _queueName; 
    private IConnection? _connection;
    private IChannel? _channel; 

    private Producer(IConfiguration configuration) 
    { 
        _configuration = configuration; 
        _queueName = _configuration["RabbitMQ:QueueName"] ?? string.Empty; 
    }

    // Static factory method to handle asynchronous initialization
    public static async Task<Producer> CreateAsync(IConfiguration configuration)
    {
        var producer = new Producer(configuration);
        await producer.InitializeConnection();
        return producer;
    }

    private async Task InitializeConnection()
    {
        int port = int.TryParse(_configuration["RabbitMQ:Port"], out int parsedPort) ? parsedPort : 5672; 

        var factory = new ConnectionFactory 
        { 
            HostName = _configuration["RabbitMQ:HostName"] ?? "localhost", 
            Port = port, 
            UserName = _configuration["RabbitMQ:UserName"] ?? "guest", 
            Password = _configuration["RabbitMQ:Password"] ?? "guest" 
        };

        // Fixed: assigned to the class field instead of using 'var' (shadowing)
        _connection = await factory.CreateConnectionAsync();
        _channel = await _connection.CreateChannelAsync();

        await _channel.QueueDeclareAsync( 
            queue: _queueName, 
            durable: true, // La cola sobrevive a reinicios del servidor 
            exclusive: false, // La cola puede ser usada por múltiples conexiones 
            autoDelete: false, // La cola no se elimina automáticamente 
            arguments: null 
        ); 
    }

    public async Task<bool> SendMessage(string pedido)
    {
        try
        {
            var body = Encoding.UTF8.GetBytes(pedido);
            
            await _channel.BasicPublishAsync( 
                exchange: string.Empty, // Exchange por defecto 
                routingKey: _queueName, // Nombre de la cola como routing key 
                body: body 
            );

            return true;
        }
        catch (Exception)
        {
            return false;
        }
    }
}