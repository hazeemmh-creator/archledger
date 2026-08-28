export type Json =
  | string
  | number
  | boolean
  | null
  | { [key: string]: Json | undefined }
  | Json[]

export type Database = {
  // Allows to automatically instantiate createClient with right options
  // instead of createClient<Database, { PostgrestVersion: 'XX' }>(URL, KEY)
  __InternalSupabase: {
    PostgrestVersion: "14.17"
  }
  public: {
    Tables: {
      contribution_types: {
        Row: {
          name: string
        }
        Insert: {
          name: string
        }
        Update: {
          name?: string
        }
        Relationships: []
      }
      contributions: {
        Row: {
          amount: number
          contribution_date: string | null
          contribution_type: string | null
          created_at: string | null
          document_url: string | null
          id: string
          partner_id: string | null
          payment_method: string | null
          project_id: string | null
          purpose: string | null
          recorded_by: string | null
          reimbursement_expected: boolean | null
          reimbursement_status: string | null
          updated_at: string | null
        }
        Insert: {
          amount?: number
          contribution_date?: string | null
          contribution_type?: string | null
          created_at?: string | null
          document_url?: string | null
          id?: string
          partner_id?: string | null
          payment_method?: string | null
          project_id?: string | null
          purpose?: string | null
          recorded_by?: string | null
          reimbursement_expected?: boolean | null
          reimbursement_status?: string | null
          updated_at?: string | null
        }
        Update: {
          amount?: number
          contribution_date?: string | null
          contribution_type?: string | null
          created_at?: string | null
          document_url?: string | null
          id?: string
          partner_id?: string | null
          payment_method?: string | null
          project_id?: string | null
          purpose?: string | null
          recorded_by?: string | null
          reimbursement_expected?: boolean | null
          reimbursement_status?: string | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "contributions_contribution_type_fkey"
            columns: ["contribution_type"]
            isOneToOne: false
            referencedRelation: "contribution_types"
            referencedColumns: ["name"]
          },
          {
            foreignKeyName: "contributions_partner_id_fkey"
            columns: ["partner_id"]
            isOneToOne: false
            referencedRelation: "partners"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "contributions_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "contributions_recorded_by_fkey"
            columns: ["recorded_by"]
            isOneToOne: false
            referencedRelation: "user_profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "contributions_reimbursement_status_fkey"
            columns: ["reimbursement_status"]
            isOneToOne: false
            referencedRelation: "reimbursement_statuses"
            referencedColumns: ["name"]
          },
        ]
      }
      expense_categories: {
        Row: {
          description: string | null
          is_active: boolean | null
          macro_category: string
          name: string
        }
        Insert: {
          description?: string | null
          is_active?: boolean | null
          macro_category: string
          name: string
        }
        Update: {
          description?: string | null
          is_active?: boolean | null
          macro_category?: string
          name?: string
        }
        Relationships: []
      }
      expenses: {
        Row: {
          category: string | null
          created_at: string | null
          description: string
          document_url: string | null
          expense_date: string | null
          gross_amount: number
          id: string
          is_deleted: boolean | null
          net_paid: number
          notes: string | null
          paid_by: string | null
          payment_method: string | null
          payment_source: string | null
          project_id: string | null
          recorded_by: string | null
          reference_number: string | null
          updated_at: string | null
          vat_paid: number | null
          vendor_payee: string | null
          wht_withheld: number | null
        }
        Insert: {
          category?: string | null
          created_at?: string | null
          description: string
          document_url?: string | null
          expense_date?: string | null
          gross_amount?: number
          id?: string
          is_deleted?: boolean | null
          net_paid?: number
          notes?: string | null
          paid_by?: string | null
          payment_method?: string | null
          payment_source?: string | null
          project_id?: string | null
          recorded_by?: string | null
          reference_number?: string | null
          updated_at?: string | null
          vat_paid?: number | null
          vendor_payee?: string | null
          wht_withheld?: number | null
        }
        Update: {
          category?: string | null
          created_at?: string | null
          description?: string
          document_url?: string | null
          expense_date?: string | null
          gross_amount?: number
          id?: string
          is_deleted?: boolean | null
          net_paid?: number
          notes?: string | null
          paid_by?: string | null
          payment_method?: string | null
          payment_source?: string | null
          project_id?: string | null
          recorded_by?: string | null
          reference_number?: string | null
          updated_at?: string | null
          vat_paid?: number | null
          vendor_payee?: string | null
          wht_withheld?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "expenses_category_fkey"
            columns: ["category"]
            isOneToOne: false
            referencedRelation: "expense_categories"
            referencedColumns: ["name"]
          },
          {
            foreignKeyName: "expenses_paid_by_fkey"
            columns: ["paid_by"]
            isOneToOne: false
            referencedRelation: "user_profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "expenses_payment_source_fkey"
            columns: ["payment_source"]
            isOneToOne: false
            referencedRelation: "payment_sources"
            referencedColumns: ["name"]
          },
          {
            foreignKeyName: "expenses_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "expenses_recorded_by_fkey"
            columns: ["recorded_by"]
            isOneToOne: false
            referencedRelation: "user_profiles"
            referencedColumns: ["id"]
          },
        ]
      }
      funding_source_types: {
        Row: {
          name: string
        }
        Insert: {
          name: string
        }
        Update: {
          name?: string
        }
        Relationships: []
      }
      funding_statuses: {
        Row: {
          name: string
        }
        Insert: {
          name: string
        }
        Update: {
          name?: string
        }
        Relationships: []
      }
      funding_transactions: {
        Row: {
          created_at: string | null
          date_received: string | null
          description: string | null
          document_url: string | null
          gross_amount: number
          id: string
          net_received: number
          payer_name: string | null
          payment_method: string | null
          project_id: string | null
          recorded_by: string | null
          reference_number: string | null
          source_type: string | null
          status: string | null
          updated_at: string | null
          vat_amount: number | null
          wht_deducted: number | null
        }
        Insert: {
          created_at?: string | null
          date_received?: string | null
          description?: string | null
          document_url?: string | null
          gross_amount?: number
          id?: string
          net_received?: number
          payer_name?: string | null
          payment_method?: string | null
          project_id?: string | null
          recorded_by?: string | null
          reference_number?: string | null
          source_type?: string | null
          status?: string | null
          updated_at?: string | null
          vat_amount?: number | null
          wht_deducted?: number | null
        }
        Update: {
          created_at?: string | null
          date_received?: string | null
          description?: string | null
          document_url?: string | null
          gross_amount?: number
          id?: string
          net_received?: number
          payer_name?: string | null
          payment_method?: string | null
          project_id?: string | null
          recorded_by?: string | null
          reference_number?: string | null
          source_type?: string | null
          status?: string | null
          updated_at?: string | null
          vat_amount?: number | null
          wht_deducted?: number | null
        }
        Relationships: [
          {
            foreignKeyName: "funding_transactions_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "funding_transactions_recorded_by_fkey"
            columns: ["recorded_by"]
            isOneToOne: false
            referencedRelation: "user_profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "funding_transactions_source_type_fkey"
            columns: ["source_type"]
            isOneToOne: false
            referencedRelation: "funding_source_types"
            referencedColumns: ["name"]
          },
          {
            foreignKeyName: "funding_transactions_status_fkey"
            columns: ["status"]
            isOneToOne: false
            referencedRelation: "funding_statuses"
            referencedColumns: ["name"]
          },
        ]
      }
      partners: {
        Row: {
          address: string | null
          created_at: string | null
          email: string | null
          full_name: string
          id: string
          phone_number: string | null
          status: string | null
        }
        Insert: {
          address?: string | null
          created_at?: string | null
          email?: string | null
          full_name: string
          id?: string
          phone_number?: string | null
          status?: string | null
        }
        Update: {
          address?: string | null
          created_at?: string | null
          email?: string | null
          full_name?: string
          id?: string
          phone_number?: string | null
          status?: string | null
        }
        Relationships: []
      }
      payment_sources: {
        Row: {
          name: string
        }
        Insert: {
          name: string
        }
        Update: {
          name?: string
        }
        Relationships: []
      }
      project_partners: {
        Row: {
          agreement_notes: string | null
          created_at: string | null
          effective_date: string | null
          id: string
          partner_id: string | null
          profit_share_percentage: number | null
          project_id: string | null
          role_in_project: string | null
        }
        Insert: {
          agreement_notes?: string | null
          created_at?: string | null
          effective_date?: string | null
          id?: string
          partner_id?: string | null
          profit_share_percentage?: number | null
          project_id?: string | null
          role_in_project?: string | null
        }
        Update: {
          agreement_notes?: string | null
          created_at?: string | null
          effective_date?: string | null
          id?: string
          partner_id?: string | null
          profit_share_percentage?: number | null
          project_id?: string | null
          role_in_project?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "project_partners_partner_id_fkey"
            columns: ["partner_id"]
            isOneToOne: false
            referencedRelation: "partners"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "project_partners_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
        ]
      }
      project_statuses: {
        Row: {
          description: string | null
          is_locked: boolean | null
          name: string
        }
        Insert: {
          description?: string | null
          is_locked?: boolean | null
          name: string
        }
        Update: {
          description?: string | null
          is_locked?: boolean | null
          name?: string
        }
        Relationships: []
      }
      projects: {
        Row: {
          approved_budget: number | null
          client_organization: string | null
          contract_value: number | null
          created_at: string | null
          created_by: string | null
          currency: string | null
          expected_completion_date: string | null
          id: string
          manager_id: string | null
          opening_financial_position: number | null
          owner_id: string | null
          project_category: string | null
          project_code: string | null
          project_description: string | null
          project_location: string | null
          project_name: string
          start_date: string | null
          status: string | null
          updated_at: string | null
        }
        Insert: {
          approved_budget?: number | null
          client_organization?: string | null
          contract_value?: number | null
          created_at?: string | null
          created_by?: string | null
          currency?: string | null
          expected_completion_date?: string | null
          id?: string
          manager_id?: string | null
          opening_financial_position?: number | null
          owner_id?: string | null
          project_category?: string | null
          project_code?: string | null
          project_description?: string | null
          project_location?: string | null
          project_name: string
          start_date?: string | null
          status?: string | null
          updated_at?: string | null
        }
        Update: {
          approved_budget?: number | null
          client_organization?: string | null
          contract_value?: number | null
          created_at?: string | null
          created_by?: string | null
          currency?: string | null
          expected_completion_date?: string | null
          id?: string
          manager_id?: string | null
          opening_financial_position?: number | null
          owner_id?: string | null
          project_category?: string | null
          project_code?: string | null
          project_description?: string | null
          project_location?: string | null
          project_name?: string
          start_date?: string | null
          status?: string | null
          updated_at?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "projects_created_by_fkey"
            columns: ["created_by"]
            isOneToOne: false
            referencedRelation: "user_profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "projects_manager_id_fkey"
            columns: ["manager_id"]
            isOneToOne: false
            referencedRelation: "user_profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "projects_owner_id_fkey"
            columns: ["owner_id"]
            isOneToOne: false
            referencedRelation: "user_profiles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "projects_status_fkey"
            columns: ["status"]
            isOneToOne: false
            referencedRelation: "project_statuses"
            referencedColumns: ["name"]
          },
        ]
      }
      reimbursement_statuses: {
        Row: {
          name: string
        }
        Insert: {
          name: string
        }
        Update: {
          name?: string
        }
        Relationships: []
      }
      system_roles: {
        Row: {
          created_at: string | null
          description: string | null
          id: string
          name: string
        }
        Insert: {
          created_at?: string | null
          description?: string | null
          id?: string
          name: string
        }
        Update: {
          created_at?: string | null
          description?: string | null
          id?: string
          name?: string
        }
        Relationships: []
      }
      user_profiles: {
        Row: {
          created_at: string | null
          full_name: string | null
          id: string
          phone_number: string | null
          status: string | null
          updated_at: string | null
        }
        Insert: {
          created_at?: string | null
          full_name?: string | null
          id: string
          phone_number?: string | null
          status?: string | null
          updated_at?: string | null
        }
        Update: {
          created_at?: string | null
          full_name?: string | null
          id?: string
          phone_number?: string | null
          status?: string | null
          updated_at?: string | null
        }
        Relationships: []
      }
      user_roles: {
        Row: {
          assigned_at: string | null
          id: string
          role_id: string | null
          user_id: string | null
        }
        Insert: {
          assigned_at?: string | null
          id?: string
          role_id?: string | null
          user_id?: string | null
        }
        Update: {
          assigned_at?: string | null
          id?: string
          role_id?: string | null
          user_id?: string | null
        }
        Relationships: [
          {
            foreignKeyName: "user_roles_role_id_fkey"
            columns: ["role_id"]
            isOneToOne: false
            referencedRelation: "system_roles"
            referencedColumns: ["id"]
          },
          {
            foreignKeyName: "user_roles_user_id_fkey"
            columns: ["user_id"]
            isOneToOne: false
            referencedRelation: "user_profiles"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Views: {
      project_cost_analytics: {
        Row: {
          macro_category: string | null
          project_id: string | null
          project_name: string | null
          total_spent: number | null
          transaction_count: number | null
        }
        Relationships: [
          {
            foreignKeyName: "expenses_project_id_fkey"
            columns: ["project_id"]
            isOneToOne: false
            referencedRelation: "projects"
            referencedColumns: ["id"]
          },
        ]
      }
    }
    Functions: {
      [_ in never]: never
    }
    Enums: {
      [_ in never]: never
    }
    CompositeTypes: {
      [_ in never]: never
    }
  }
}

type DatabaseWithoutInternals = Omit<Database, "__InternalSupabase">

type DefaultSchema = DatabaseWithoutInternals[Extract<keyof Database, "public">]

export type Tables<
  DefaultSchemaTableNameOrOptions extends
    | keyof (DefaultSchema["Tables"] & DefaultSchema["Views"])
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
        DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? (DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"] &
      DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Views"])[TableName] extends {
      Row: infer R
    }
    ? R
    : never
  : DefaultSchemaTableNameOrOptions extends keyof (DefaultSchema["Tables"] &
        DefaultSchema["Views"])
    ? (DefaultSchema["Tables"] &
        DefaultSchema["Views"])[DefaultSchemaTableNameOrOptions] extends {
        Row: infer R
      }
      ? R
      : never
    : never

export type TablesInsert<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Insert: infer I
    }
    ? I
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Insert: infer I
      }
      ? I
      : never
    : never

export type TablesUpdate<
  DefaultSchemaTableNameOrOptions extends
    | keyof DefaultSchema["Tables"]
    | { schema: keyof DatabaseWithoutInternals },
  TableName extends DefaultSchemaTableNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"]
    : never = never,
> = DefaultSchemaTableNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaTableNameOrOptions["schema"]]["Tables"][TableName] extends {
      Update: infer U
    }
    ? U
    : never
  : DefaultSchemaTableNameOrOptions extends keyof DefaultSchema["Tables"]
    ? DefaultSchema["Tables"][DefaultSchemaTableNameOrOptions] extends {
        Update: infer U
      }
      ? U
      : never
    : never

export type Enums<
  DefaultSchemaEnumNameOrOptions extends
    | keyof DefaultSchema["Enums"]
    | { schema: keyof DatabaseWithoutInternals },
  EnumName extends DefaultSchemaEnumNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"]
    : never = never,
> = DefaultSchemaEnumNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[DefaultSchemaEnumNameOrOptions["schema"]]["Enums"][EnumName]
  : DefaultSchemaEnumNameOrOptions extends keyof DefaultSchema["Enums"]
    ? DefaultSchema["Enums"][DefaultSchemaEnumNameOrOptions]
    : never

export type CompositeTypes<
  PublicCompositeTypeNameOrOptions extends
    | keyof DefaultSchema["CompositeTypes"]
    | { schema: keyof DatabaseWithoutInternals },
  CompositeTypeName extends PublicCompositeTypeNameOrOptions extends {
    schema: keyof DatabaseWithoutInternals
  }
    ? keyof DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"]
    : never = never,
> = PublicCompositeTypeNameOrOptions extends {
  schema: keyof DatabaseWithoutInternals
}
  ? DatabaseWithoutInternals[PublicCompositeTypeNameOrOptions["schema"]]["CompositeTypes"][CompositeTypeName]
  : PublicCompositeTypeNameOrOptions extends keyof DefaultSchema["CompositeTypes"]
    ? DefaultSchema["CompositeTypes"][PublicCompositeTypeNameOrOptions]
    : never

export const Constants = {
  public: {
    Enums: {},
  },
} as const
