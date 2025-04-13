Порядок выполнения контрольного задания:

### Конфигурирование коммутатора.

1. Конфигурирование VLAN на коммутаторе
  
    [hint]
    ```
    MES1(config-vlan)#  vlan 4 name v4
    MES1(config-vlan)# exit
    MES1(config)# exit
    ```
    [/hint]

2. Настройка access-портов

    [hint]
    ```
    MES1# configure
    MES1(config)# interface GigabitEthernet 1/0/4
    MES1(config-if)# switchport mode access
    MES1(config-if)# switchport access vlan 4
    MES1(config-if)# exit
    ```
    [/hint]

3. Настройка trunk-портов

    [hint]
    ```
    MES1(config)# interface GigabitEthernet 1/0/3
    MES1(config-if)# switchport mode trunk
    MES1(config-if)# switchport trunk allowed vlan add 3,4
    MES1(config-if)# exit
    ```
    [/hint]

### Конфигурирование маршрутизатора.

1. Смена режима интерфейса на routerport

    [hint]
    ```
    esr-1# configure
    esr-1(config)# interface gigabitethernet 1/0/2
    esr-1(config-if-gi)# mode routerport
    esr-1(config-if-gi)# exit
    esr-1(config)# exit
    ```
    [/hint]

2. Назначение IP-адреса интерфейса внешней сети

    [hint]
    ```
    esr-1# configure
    esr-1(config)# interface gigabitethernet 1/0/2
    esr-1(config-if-gi)# ip address 192.168.2.1/24
    esr-1(config-if-gi)# ip firewall disable
    esr-1(config-if-gi)# end
    ```
    [/hint]

3. Конфигурирование sub-интерфейсов (внутренняя сеть)

    [hint]
    ```
    esr-1(config)# interface gigabitethernet 1/0/3.4
    esr-1(config-subif)# ip address 192.168.4.10/24
    esr-1(config-subif)# ip firewall disable
    esr-1(config-subif)# end
    ```
    [/hint]

4. Конфигурирование протокола OSPF

    [hint]
    ```
    esr-1# configure
    esr(config)# router ospf 10
    esr(config-ospf)# redistribute connected
    esr-1(config-ospf)# area 1.1.1.1
    esr-1(config-ospf-area)# network 192.168.2.0/24
    esr-1(config-ospf-area)# enable
    esr-1(config-ospf-area)# exit
    esr-1(config-ospf)# enable
    esr-1(config-ospf)# exit
    ```
    [/hint]

5. Конфигурирование протокола IS-IS

    [hint]
    ```
    esr-1# configure
    esr-1(config)# router isis 1
    esr-1(config-isis)# redistribute connected
    esr-1(config-isis)# net 49.0001.1111.1111.1111.00
    esr-1(config-isis)# is-type level-1
    esr-1(config-isis)# metric-style narrow level-1
    esr-1(config-isis)# enable
    ```
    [/hint]

6. Конфигурирование OSPF на физических интерфейсах

    [hint]
    ```
    esr-1(config)# interface gigabitethernet 1/0/2
    esr-1(config-if-gi)# ip ospf instance 10
    esr-1(config-if-gi)# ip ospf area 1.1.1.1
    esr-1(config-if-gi)# ip ospf
    esr-1(config-if-gi)# exit
    ```
    [/hint]

7. Конфигурирование IS-IS на физических интерфейсах 

    [hint]
    ```
    esr-1# configure
    esr-1(config)# interface gigabitethernet 1/0/2
    esr-1(config-if-gi)# isis instance 1
    esr-1(config-if-gi)# isis enable
    esr-1(config-if-gi)# exit
    esr-1(config)# exit
    ```
    [/hint]
