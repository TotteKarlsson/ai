object MainForm: TMainForm
  Left = 0
  Top = 0
  Caption = 'TSC Printer Tester'
  ClientHeight = 314
  ClientWidth = 548
  Color = clBtnFace
  Font.Charset = DEFAULT_CHARSET
  Font.Color = clWindowText
  Font.Height = -11
  Font.Name = 'Tahoma'
  Font.Style = []
  KeyPreview = True
  OldCreateOrder = False
  OnKeyDown = FormKeyDown
  PixelsPerInch = 96
  TextHeight = 13
  object Button1: TButton
    Left = 456
    Top = 16
    Width = 84
    Height = 39
    Caption = 'About'
    TabOrder = 0
    OnClick = Button1Click
  end
  object Button2: TButton
    Left = 24
    Top = 72
    Width = 177
    Height = 57
    Caption = 'Print'
    TabOrder = 1
    OnClick = Button2Click
  end
  object mInfoMemo: TMemo
    Left = 0
    Top = 145
    Width = 548
    Height = 169
    Align = alBottom
    Lines.Strings = (
      'mInfoMemo')
    TabOrder = 2
  end
  object mDataStr: TSTDStringLabeledEdit
    Left = 24
    Top = 34
    Width = 121
    Height = 21
    EditLabel.Width = 23
    EditLabel.Height = 13
    EditLabel.Caption = 'Data'
    TabOrder = 3
    Text = 'M-123456'
    Value = 'M-123456'
  end
  object mCopies: TIntegerLabeledEdit
    Left = 168
    Top = 34
    Width = 121
    Height = 21
    EditLabel.Width = 32
    EditLabel.Height = 13
    EditLabel.Caption = 'Copies'
    TabOrder = 4
    Text = '1'
    Value = 1
  end
end
