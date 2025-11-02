using Microsoft.Win32;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Windows;

namespace Task1
{
    public partial class MainWindow : Window
    {
        private List<double> originalList = new List<double>();
        private List<double> processedList = new List<double>();

        public MainWindow()
        {
            InitializeComponent();
        }

        private void LoadButton_Click(object sender, RoutedEventArgs e)
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "Текстові файли (*.txt)|*.txt|Всі файли (*.*)|*.*";

            if (openFileDialog.ShowDialog() == true)
            {
                try
                {
                    string filePath = openFileDialog.FileName;
                    originalList.Clear();

                    string[] lines = File.ReadAllLines(filePath);
                    foreach (string line in lines)
                    {
                        string[] numbers = line.Split(new[] { ' ', '\t' }, System.StringSplitOptions.RemoveEmptyEntries);
                        foreach (string numStr in numbers)
                        {
                            if (double.TryParse(numStr, System.Globalization.NumberStyles.Float, System.Globalization.CultureInfo.InvariantCulture, out double number))
                            {
                                originalList.Add(number);
                            }
                        }
                    }

                    DisplayList(originalList, OriginalListBox);
                    ProcessedListBox.Items.Clear();
                    ProcessSaveButton.IsEnabled = true;
                }
                catch (IOException ex)
                {
                    MessageBox.Show($"Помилка читання файлу: {ex.Message}", "Помилка", MessageBoxButton.OK, MessageBoxImage.Error);
                }
                catch (System.Exception ex)
                {
                    MessageBox.Show($"Виникла помилка: {ex.Message}", "Помилка", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }

        private void ProcessSaveButton_Click(object sender, RoutedEventArgs e)
        {
            if (originalList.Count == 0)
            {
                MessageBox.Show("Список порожній. Будь ласка, спочатку завантажте дані.", "Увага", MessageBoxButton.OK, MessageBoxImage.Warning);
                return;
            }

            processedList = ProcessList(originalList);

            DisplayList(processedList, ProcessedListBox);

            SaveListToFile(processedList);
        }

        private List<double> ProcessList(List<double> inputList)
        {
            var nonNegative = inputList.Where(n => n >= 0).ToList();

            var negative = inputList.Where(n => n < 0).ToList();
            negative.Reverse();

            return nonNegative.Concat(negative).ToList();
        }

        private void DisplayList(List<double> list, System.Windows.Controls.ListBox listBox)
        {
            listBox.Items.Clear();
            foreach (var item in list)
            {
                listBox.Items.Add(item.ToString(System.Globalization.CultureInfo.InvariantCulture));
            }
        }

        private void SaveListToFile(List<double> list)
        {
            SaveFileDialog saveFileDialog = new SaveFileDialog();
            saveFileDialog.Filter = "Текстові файли (*.txt)|*.txt|Всі файли (*.*)|*.*";

            if (saveFileDialog.ShowDialog() == true)
            {
                try
                {
                    string filePath = saveFileDialog.FileName;
                    StringBuilder sb = new StringBuilder();

                    for (int i = 0; i < list.Count; i++)
                    {
                        sb.Append(list[i].ToString(System.Globalization.CultureInfo.InvariantCulture));

                        if ((i + 1) % 10 == 0 || i == list.Count - 1)
                        {
                            sb.AppendLine();
                        }
                        else
                        {
                            sb.Append(" ");
                        }
                    }

                    File.WriteAllText(filePath, sb.ToString());
                    MessageBox.Show("Файл успішно збережено!", "Виконано", MessageBoxButton.OK, MessageBoxImage.Information);
                }
                catch (IOException ex)
                {
                    MessageBox.Show($"Помилка збереження файлу: {ex.Message}", "Помилка", MessageBoxButton.OK, MessageBoxImage.Error);
                }
            }
        }
    }
}

