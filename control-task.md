Порядок выполнения контрольного задания:

### Конфигурирование коммутатора.

1. Создание VLAN на коммутаторе
  
  [hint]```
  # vlan database
  (vlan)# vlan X name VLAN-X-NAME
  ```
  [/hint]

2. Настройка access-портов

  [hint]```
  interface FastEthernet1/1
    switchport access vlan 10
  ```
  [/hint]

3. Настройка trunk-портов

  [hint]```
  interface FastEthernet1/0
    switchport mode trunk
  ```
  [/hint]

### Конфигурирование маршрутизатора.

1. Конфигурирование sub-интерфейсов (внутренняя сеть)

  [hint]```
  interface gigabitethernet 1/0/6.10
    ip firewall disable
    ip address 10.10.1.2/30
  exit
  ```
  [/hint]

2. Конфигурирование протокола OSPF

  [hint]```
  router ospf 1 
    router-id 1.1.1.1
    redistribute connected
    area 0.0.0.0
      enable
    exit
    enable
  exit
  ```
  [/hint]


3. Конфигурирование протокола IS-IS

  [hint]```
  router isis 1
    net 49.0001.0000.0000.0001.00
    redistribute connected
    enable
  exit
  ```
  [/hint]

4. Конфигурирование интерфейса внешней сети (протокол OSPF)

  [hint]```
  interface gigabitethernet 1/0/8
    ip firewall disable
    ip address 10.10.1.21/30
    ip ospf instance 1
    ip ospf
  exit
  ```
  [/hint]

5. Конфигурирование интерфейса внешней сети (протокол IS-IS)

  [hint]```
  interface gigabitethernet 1/0/8
    ip firewall disable
    ip address 10.10.1.25/30
    isis instance 1
    isis enable
  ```
  [/hint]

### Задание IP-адреса абонентским устройствам.

[hint]```
PC1> ip 10.10.1.1/30 10.10.1.2
```
[/hint]

### Сброс настроек на маршрутизаторе.

[hint]```
# copy system:factory-config system:candidate-config
# commit
# confirm
```
[/hint]
