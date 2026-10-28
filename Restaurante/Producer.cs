using System; 
using System.Text;
using Microsoft.Extensions.Configuration;
using RabbitMQ.Client; 

class Producer
{
    private readonly IConfiguration _configuration; 
    private readonly string _queueName; 
    private IChannel? _channel; 

    public Producer(IConfiguration configuration) { 
     _configuration = configuration; 
     _queueName = _configuration["RabbitMQ:QueueName"]; // Se obtiene el valor desde appsettings.json 
     int port =  int.TryParse(_configuration["RabbitMQ:Port"], out int parsedPort) ? parsedPort : 5672; 
      } 

      

    
}