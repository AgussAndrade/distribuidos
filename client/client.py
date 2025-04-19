import time
import json
from typing import Generator
from middleware.producer.producer import Producer
from middleware.consumer.consumer import Consumer

class Client:
    def __init__(self, batch_size: int = 10):
        self.producer = Producer("movie")
        self.producer_1 = Producer("movie_1")
        self.consumer = Consumer("result")
        self.batch_size = batch_size

    def wait_for_result(self, expected_results: int = 5, timeout: int = 30) -> bool:
        """Espera por un número específico de resultados de la cola 'result' con timeout configurable"""
        start_time = time.time()
        retry_interval = 0.1  # 100ms entre intentos
        results_received = 0
        
        while time.time() - start_time < timeout:
            result = self.consumer.dequeue()
            if result:
                results_received += 1
                print(f"[INFO] Resultado {results_received}/{expected_results} recibido: {result}")
                if results_received >= expected_results:
                    return True
            time.sleep(retry_interval)
        
        print(f"[ERROR] Timeout esperando resultados. Recibidos: {results_received}/{expected_results}")
        return False

    def close(self):
        """Cierra las conexiones"""
        self.producer.close()
        self.consumer.close()

    def send(self, message: dict) -> (bool, bool):
        """Envía un mensaje y maneja errores"""
        try:
            print(f"[CLIENT] Enviando mensaje: {message}")
            return (self.producer.enqueue(message),self.producer_1.enqueue(message))
        except Exception as e:
            print(f"[ERROR] Error al enviar mensaje: {e}")
            return (False, False)

    def process_file(self, file_path: str) -> Generator[tuple[list[str], bool], None, None]:
        """Procesa el archivo en lotes de manera eficiente"""
        try:
            with open(file_path, "r") as file:
                # Leer el encabezado
                header = next(file)
                current_batch = []
                # Leer la primera línea después del header
                line = next(file, None)
                
                while line is not None:
                    current_batch.append(line)
                    
                    # Leer la siguiente línea para ver si es la última
                    next_line = next(file, None)
                    is_last = next_line is None
                    
                    if len(current_batch) >= self.batch_size or is_last:
                        yield [header] + current_batch, is_last
                        current_batch = []
                    
                    line = next_line
        finally:
            file.close()

def wait_for_rabbitmq(max_retries: int = 30, retry_interval: float = 1.0) -> bool:
    """Espera a que RabbitMQ esté disponible"""
    for _ in range(max_retries):
        try:
            producer = Producer("test")
            if producer.connect():
                producer.close()
                return True
        except Exception:
            pass
        time.sleep(retry_interval)
    return False

if __name__ == '__main__':
    if not wait_for_rabbitmq():
        print("[ERROR] No se pudo conectar con RabbitMQ después de varios intentos")
        exit(1)

    client = Client(batch_size=100)
    successful_batches = 0
    total_batches = 0

    try:
        for batch, is_last in client.process_file("root/files/movies.txt"):
            message = {
                "type": "movie",
                "cola": batch,
                "batch_size": len(batch),
                "total_batches": total_batches + len(batch) if is_last else 0
            }
            result_0, result_1 = client.send(message)

            if result_0 or result_1:
                successful_batches += 1
                print(f"[MAIN] Batch {total_batches + 1} enviado correctamente")
            else:
                print(f"[ERROR] Falló el envío del batch {total_batches + 1}")
            total_batches += len(batch)
        
        # Esperar por 5 resultados (uno por cada filtro)
        if not client.wait_for_result(expected_results=2, timeout=1000):
            print(f"[WARNING] Timeout esperando resultados finales")

    except Exception as e:
        print(f"[ERROR] Error durante el procesamiento: {e}")
    finally:
        print(f"\nResumen:")
        print(f"Total de lotes procesados: {total_batches}")
        print(f"Lotes exitosos: {successful_batches}")
        print(f"Tasa de éxito: {(successful_batches/total_batches)*100:.2f}%")
        client.close()
